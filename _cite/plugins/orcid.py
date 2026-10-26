import json
from urllib.request import Request, urlopen
from util import *
from manubot.cite.handlers import prefix_to_handler as manubot_prefixes


def main(entry):
    """
    receives single list entry from orcid data file
    returns list of sources to cite
    """

    # orcid api
    endpoint = "https://pub.orcid.org/v3.0/$ORCID/works"
    headers = {"Accept": "application/json"}

    # get id from entry
    _id = get_safe(entry, "orcid", "")
    if not _id:
        raise Exception('No "orcid" key')

    # query api
    @log_cache
    @cache.memoize(name=__file__, expire=1 * (60 * 60 * 24))
    def query(_id):
        url = endpoint.replace("$ORCID", _id)
        request = Request(url=url, headers=headers)
        response = json.loads(urlopen(request).read())
        return get_safe(response, "group", [])

    response = query(_id)

    # list of sources to return
    sources = []

    # go through response structure and pull out ids e.g. doi:1234/56789
    for work in response:
        # get list of ids
        ids = []
        for summary in get_safe(work, "work-summary", []):
            ids = ids + get_safe(summary, "external-ids.external-id", [])

        # find first id of particular "relationship" type
        relationships = ["self", "version-of", "part-of"]
        related = [
            id
            for id in ids
            if get_safe(id, "external-id-relationship", "") in relationships
        ]
        # prefer ids of the work itself that Manubot can cite (e.g. doi over
        # orcid-internal source-work-id), not "part-of" ids like a proceedings isbn
        citeable = [
            id
            for id in ids
            if get_safe(id, "external-id-relationship", "") == "self"
            and get_safe(id, "external-id-type", "") in manubot_prefixes
        ]
        _id = next(
            iter(citeable + related),
            ids[0] if len(ids) > 0 else None,
        )

        if _id == None:
            continue

        # get id and id-type from response
        id_type = get_safe(_id, "external-id-type", "")
        id_value = get_safe(_id, "external-id-value", "")

        # create source
        source = {"id": f"{id_type}:{id_value}"}

        # if not an id type that Manubot can cite, keep citation details
        if id_type not in manubot_prefixes:
            # get summaries
            summaries = get_safe(work, "work-summary", [])

            # get first summary with defined sub-value
            def first(get_func):
                return next(
                    (value for value in map(get_func, summaries) if value), None
                )

            # get title
            title = first(lambda s: get_safe(s, "title.title.value", ""))

            # get publisher
            publisher = first(lambda s: get_safe(s, "journal-title.value", ""))

            # get publication date, e.g. 2011 or 2011-03 or 2011-03-05
            def publication_date(summary):
                parts = [
                    get_safe(summary, f"publication-date.{part}.value", "")
                    for part in ["year", "month", "day"]
                ]
                parts = [part for part in parts if part]
                # pad missing month/day so date sorts and formats correctly
                parts = parts + ["01"] * (3 - len(parts)) if parts else []
                return "-".join(parts)

            # get date (prefer publication date over record modified/created dates)
            date = (
                first(publication_date)
                or get_safe(work, "last-modified-date.value")
                or first(lambda s: get_safe(s, "last-modified-date.value"))
                or get_safe(work, "created-date.value")
                or first(lambda s: get_safe(s, "created-date.value"))
                or 0
            )

            # get link, falling back to a link built from any external id
            def id_link(id):
                url = get_safe(id, "external-id-url.value", "")
                if url:
                    return url
                if get_safe(id, "external-id-type", "") == "doi":
                    return "https://doi.org/" + get_safe(id, "external-id-value", "")
                return ""

            link = first(lambda s: get_safe(s, "url.value", "")) or next(
                (url for url in map(id_link, ids) if url), None
            )

            # keep available details
            if title:
                source["title"] = title
            if publisher:
                source["publisher"] = publisher
            if date:
                source["date"] = format_date(date)
            if link:
                source["link"] = link

        # copy fields from entry to source
        source.update(entry)

        # add source to list
        sources.append(source)

    return sources

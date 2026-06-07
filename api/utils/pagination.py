from urllib.parse import urlencode

def build_links(base_url, args, limit, offset, count):
    links = {}

    def build_url(new_offset):
        params = args.copy()

        params["_limit"] = limit
        params["_offset"] = new_offset

        return f"{base_url}?{urlencode(params)}"

    links["_first"] = {
        "href": build_url(0)
    }

    if offset > 0:
        prev_offset = max(offset - limit, 0)
        links["_prev"] = {
            "href": build_url(prev_offset)
        }

    if offset + limit < count:
        next_offset = offset + limit
        links["_next"] = {
            "href": build_url(next_offset)
        }

    last_offset = (count - 1) // limit * limit if count > 0 else 0
    links["_last"] = {
        "href": build_url(last_offset)
    }

    return links
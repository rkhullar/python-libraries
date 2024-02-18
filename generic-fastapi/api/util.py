def build_filter_params(filter_parts: list[dict]) -> dict:
    match len(filter_parts):
        case 0:
            return dict()
        case 1:
            return filter_parts[0]
        case _:
            return {'$and': filter_parts}

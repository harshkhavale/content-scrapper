def filter_results(results, search_term):
    if search_term:
        return [result for result in results if search_term.lower() in result['title'].lower()]
    return results

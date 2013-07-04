
def RemoveContent(content_list, content_name):
    """Remove first instance of content object from the given list.

    Args:
      content_list: List of string names of objects.
      content_name: Name of the object to be removed from the room.

    Returns:
      The object if found, None otherwise.
    """
    for i, c in enumerate(content_list):
        if c == content_name:
            break
    if i == len(content_list)-1 and c != content_name:
        return None
    return content_list.pop(i)


def GetContentsDisplay(content_list):
    """Return a readable list of contents of a list of  objects.

    Args:
      content_list: List of string names of objects.

    Returns:
      A list of strings of the form "NxNAME" where N is the number of that
      object in the list.  [] if there are no objects in the list.
    """
    counts = {}
    for content in content_list:
        if not content in counts:
            counts[content] = 0
        counts[content] += 1
    output = []
    for n, c in counts.iteritems():
        output.append((n, c))
    output.sort(key=lambda x: x[0])
    return ["%dx%s" % (c, n) for n, c in output]


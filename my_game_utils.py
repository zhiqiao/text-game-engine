def RemoveContent(content_list, content_name):
    """Remove first instance of content object from the given list.

    Use of this method instead of Python's list.remove() is to remain consistent
    with stated goal of having game interactions return None on invalid state,
    not raise an error.

    This could just as easily be changed to use list.remove().

    Args:
      content_list: List of string names of objects.
      content_name: Name of the object to be removed from the room.

    Returns:
      The object if found, None otherwise.
    """
    i = -1  # For the degenerate case of an empty list.
    for i, c in enumerate(content_list):
        if c == content_name:
            break
    if i == -1 or i == len(content_list)-1 and c != content_name:
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


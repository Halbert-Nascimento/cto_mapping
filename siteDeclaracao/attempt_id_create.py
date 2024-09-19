import uuid


def attempt_id_create(session_id):
    attempt_id = str(uuid.uuid4()) # generate a random UUID
    attempt_id = attempt_id.replace("-", "") # remove the hyphens
    attempt_id = attempt_id[:20] # take the first 8 characters
    attempt_id = session_id+'-'+attempt_id  # append the session_id
    return attempt_id # return the attempt_id
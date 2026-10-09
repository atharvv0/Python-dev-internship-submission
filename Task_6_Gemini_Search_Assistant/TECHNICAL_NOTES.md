# Technical Notes

## Conversation memory

Each successful interaction returns an interaction ID. That ID is stored in `previous_id` and passed to the next call as `previous_interaction_id`, allowing Gemini to continue the same conversation without resending the entire history.

## Real-time information

The project uses Gemini's `google_search` tool. When enabled, Gemini can search public web content, synthesize the results, and expose URL citations in the response metadata.

## Security

API credentials are stored in `.env` and excluded by the root `.gitignore`.

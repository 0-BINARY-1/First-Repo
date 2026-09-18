# Stage A — what these words mean

Write these in your own words after you run the scripts. Below is a starter you can rewrite.

## Message

A **message** is one turn in the conversation you send to the model. It has a `role` (`system`, `user`, or `assistant`) and `content` (the text). The `system` message is the job description. The `user` message is the request. Previous `assistant` messages are history you choose to send back.

## Token

A **token** is a chunk of text the model reads or writes — roughly a short word or part of a word. You pay per token. The **context window** is the maximum number of tokens the model can see at once (prompt + reply).

## Tool

A **tool** is a function *your code* can run when the model asks for it (search, read a file, call an API). This project has **no tools**. That comes in Stage C. Until then, the model can only talk, not act.

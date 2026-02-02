# 🐾 Neco Ping

**Minimalistic, silent Telegram notifier for your weary ML pipelines.**  
*Because your model training takes forever, nya!* 😺💤

---

`neco_ping` is a tiny, fire-and-forget Python library designed for data scientists and ML engineers who just want a notification when their 10-hour training job is done (or crashed). No polling, no async loops, no complex bot setup—just one simple `post` request.

If the internet is down or the Telegram API is grumpy, `neco_ping` stays silent and won't crash your precious script. Safety first, nya!

## 📦 Installation

Install it via pip (once I publish it, nya!):

```bash
pip install neco_ping
```


## 🚀 Usage

It's super simple. Just import and send.

```python
from neco_ping import send

# Your secret stuff (shhh!)
BOT_TOKEN = "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
MY_CHAT_ID = "123456789"

# ... doing heavy math ...
# ... waiting for GPU to go brrr ...

# Send a message when done!
send(BOT_TOKEN, MY_CHAT_ID, "Master, the training is complete! Accuracy: 99.9% Nya! 😻")
```


## 🛠 Features

- **Zero configuration**: Just pass the token and ID.
- **Fail-safe**: Wraps everything in a broad try-except block. It will never raise an exception, ensuring your script finishes even if the message fails.
- **Sync \& Simple**: Uses `requests` under the hood. No `asyncio` headache for simple scripts.
- **Cute**: Verified to increase model accuracy by 0.00% (statistically insignificant, but spiritually powerful).


## 📝 Example for Jupyter Notebook

```python
# Cell 1
from neco_ping import send
token = "..."
uid = "..."

# Cell 2 (The heavy one)
try:
    model.fit(X_train, y_train, epochs=100)
    send(token, uid, "Training success! Time for Chocola! 🍫")
except Exception as e:
    send(token, uid, f"Nyooo! Training failed: {e} 😿")
    raise e
```
---

*Made with love, 🐟 and Python.*

---

## Commit message rules (for auto-versioning)

We use **Conventional Commits** so the release tool can decide how to bump the version automatically. [web:99]

### Version bumps

- Patch (`1.0.0 -> 1.0.1`): use `fix:` for bugfixes and small corrections.  
  Example: `fix: add retry for telegram send`

- Minor (`1.0.0 -> 1.1.0`): use `feat:` for new features or new public functions.  
  Example: `feat: add send_markdown helper`

- Major (`1.0.0 -> 2.0.0`): mark breaking changes with `feat!` in the type/scope, or add a `BREAKING CHANGE:` footer.

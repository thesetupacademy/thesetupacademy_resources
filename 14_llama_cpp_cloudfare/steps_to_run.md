# Host a Localhost App with Cloudflare

## Step 1: Open Cloudflare Quick Tunnels

Go to:

https://try.cloudflare.com/

---

## Step 2: Install Cloudflared

Download and install **cloudflared** for your operating system.

Verify the installation:

```bash
cloudflared --version
```

---

## Step 3: Start Your Localhost App

First, make sure your application is running locally.

For example, if your application is running on:

http://localhost:3000

Keep the application running in your terminal.

You can verify it by opening the localhost URL in your browser.

---

## Step 4: Create a Cloudflare Quick Tunnel

Open a **new terminal** and run:

```bash
cloudflared tunnel --url http://localhost:3000
```

Replace `3000` with the port your application is using.

For example:

```bash
cloudflared tunnel --url http://localhost:8080
```

---

## Step 5: Copy the Public URL

After starting the tunnel, Cloudflare will generate a temporary public URL similar to:

https://example-random-name.trycloudflare.com

Copy this URL.

Your localhost application is now accessible from the internet through this URL.

---

## Step 6: Open the Public URL

Paste the generated URL into your browser:

https://example-random-name.trycloudflare.com

You should see the same application that is running on your localhost.

---

## Step 7: Share the URL

You can now share the Cloudflare URL with others.

For example:

https://example-random-name.trycloudflare.com

Anyone with the URL can access your application while the Cloudflare tunnel is running.

---

## Step 8: Stop the Tunnel

To stop the tunnel, go back to the terminal where `cloudflared` is running and press:

```text
Ctrl + C
```

The public URL will stop working.

---

## Complete Command

For a localhost application running on port `3000`, the complete command is:

```bash
cloudflared tunnel --url http://localhost:3000
```

That's it — your localhost application is now publicly accessible through a temporary Cloudflare Quick Tunnel.

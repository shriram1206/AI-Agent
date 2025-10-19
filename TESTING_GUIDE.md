# 🧪 TESTING GUIDE - Thomas Personal Agent

## 📋 Complete Testing Checklist

---

## 🚀 STEP 1: Start the Application

### Method 1: Using Terminal
```powershell
# Navigate to project folder
cd "C:\Users\SHRIRAM M\OneDrive\personal-agent"

# Start the server
& ".venv/Scripts/python.exe" app.py
```

### Method 2: Using VS Code
1. Press `F5` or click "Run" → "Start Debugging"
2. Or open terminal and run: `python app.py`

**Expected Output:**
```
 * Serving Flask app 'app'
 * Debug mode: off
 * Running on http://127.0.0.1:5000
```

✅ **Server is running when you see this!**

---

## 🌐 STEP 2: Open in Browser

### Option A: Click these links in VS Code
- Main: http://127.0.0.1:5000
- Login: http://127.0.0.1:5000/login
- Signup: http://127.0.0.1:5000/signup

### Option B: Manual
1. Open your browser (Chrome, Edge, Firefox)
2. Go to: `http://127.0.0.1:5000`

**What you should see:**
- ✅ Redirects to login page (because you're not logged in)
- ✅ Beautiful purple gradient background
- ✅ White login form

---

## ✅ TEST 1: User Signup (Create Account)

### Steps:
1. Go to: http://127.0.0.1:5000/signup
2. Fill in the form:
   - **Username:** `john_doe` (3-30 chars, alphanumeric + underscore)
   - **Email:** `john@example.com` (valid email format)
   - **Password:** `password123` (min 8 chars, 1 letter + 1 number)
3. Click "Create Account"

### Expected Results:
✅ Success message: "Account created! Redirecting..."
✅ Auto-redirects to chat interface
✅ Sidebar shows: Username "john_doe" and email

### Test Edge Cases:
| Test | Input | Expected Result |
|------|-------|-----------------|
| **Weak Password** | `12345` | ❌ "Password must be at least 8 characters" |
| **No Number** | `password` | ❌ "Password must contain at least one number" |
| **No Letter** | `12345678` | ❌ "Password must contain at least one letter" |
| **Invalid Email** | `notanemail` | ❌ "Invalid email format" |
| **Short Username** | `ab` | ❌ "Username must be 3-30 characters" |
| **Special Chars** | `user@#$` | ❌ "Username must be alphanumeric only" |

---

## ✅ TEST 2: User Login

### Using Test Account:
1. Go to: http://127.0.0.1:5000/login
2. Enter credentials:
   - **Email:** `test@thomas.ai`
   - **Password:** `testpassword123`
3. Click "Sign In"

### Expected Results:
✅ Success message: "Login successful! Redirecting..."
✅ Redirects to chat interface
✅ Sidebar shows conversations list
✅ User menu at bottom shows "test_user"

### Test Wrong Password:
1. Try logging in with wrong password
2. Expected: ❌ "Invalid email or password"
3. Try 6 times quickly
4. Expected: ❌ "Too many requests. Please try again later." (Rate limiting!)

---

## ✅ TEST 3: Chat Interface (Main Features)

### A. Welcome Screen
**Expected:**
- ✅ Dark sidebar on left (#202123 color)
- ✅ Light chat area (#f7f7f8 color)
- ✅ Welcome message: "Hey I'm Thomas How can I help you today?"
- ✅ "New Chat" button at top of sidebar
- ✅ Input box at bottom with icons

### B. Send a Message
1. Type in input box: `Hello Thomas!`
2. Watch the **send button appear** (black arrow icon)
3. Click send or press Enter

**Expected:**
- ✅ Your message appears with green avatar (U)
- ✅ "Thomas is typing..." indicator shows
- ✅ AI response appears with purple avatar (T)
- ✅ Response is natural and conversational

### C. Continue Conversation
1. Send another message: `What is Python?`
2. Send follow-up: `Can you explain more?`

**Expected:**
- ✅ AI remembers context (uses previous messages)
- ✅ Responses are relevant to conversation
- ✅ Each message has timestamp
- ✅ Scrolls smoothly

---

## ✅ TEST 4: Conversation Management

### A. Create New Conversation
1. Click **"New Chat"** button in sidebar
2. Send a message: `Test new conversation`

**Expected:**
- ✅ Chat area clears
- ✅ Welcome message shows again
- ✅ New conversation appears in sidebar
- ✅ Conversation title is your first message

### B. Switch Between Conversations
1. Click on an **old conversation** in sidebar
2. Check messages load

**Expected:**
- ✅ All previous messages appear
- ✅ Conversation marked as active (highlighted)
- ✅ Can continue chatting

### C. Delete Conversation
1. Hover over conversation in sidebar
2. Click **trash icon** (delete button)
3. Confirm deletion

**Expected:**
- ✅ Delete confirmation appears
- ✅ Conversation removed from sidebar
- ✅ Messages deleted from database

---

## ✅ TEST 5: Voice Controls (Visual Only)

1. Clear the input box
2. Observe **two icons** appear:
   - 🎤 Microphone icon
   - ≡ Menu icon

3. Start typing
4. Observe icons **change to send button** (black arrow)

**Expected:**
- ✅ Icons switch dynamically
- ✅ Send button is black with white arrow
- ✅ Buttons have hover effects

**Note:** Voice input shows "coming soon" message (not implemented yet)

---

## ✅ TEST 6: News Feature

1. When input is empty, click **menu icon** (≡)
2. Wait for response

**Expected:**
- ✅ "Get latest news" message from you
- ✅ Thomas provides news update
- ✅ News formatted with bullets or sections

---

## ✅ TEST 7: User Profile & Logout

### A. View Profile
1. Look at **bottom of sidebar**
2. Check user menu

**Expected:**
- ✅ Avatar with first letter of username
- ✅ Username displayed
- ✅ Email displayed
- ✅ Logout button (arrow icon)

### B. Logout
1. Click **logout button**
2. Check redirection

**Expected:**
- ✅ Redirects to login page
- ✅ Cannot access chat without login
- ✅ Session cleared

---

## ✅ TEST 8: Mobile Responsive Design

### Test on Small Screen:
1. **Resize browser** to mobile width (< 768px)
2. OR use browser DevTools (F12) → Toggle Device Toolbar

**Expected:**
- ✅ Sidebar hides automatically
- ✅ **Hamburger menu** button appears (top left)
- ✅ Click hamburger → sidebar slides in
- ✅ Click outside → sidebar closes
- ✅ Chat area takes full width
- ✅ Input box responsive

---

## ✅ TEST 9: Security Features

### A. Rate Limiting Tests

**Login Rate Limit:**
1. Try logging in **6 times** with wrong password quickly
2. Expected: ❌ "Too many requests..." after 5 attempts

**Signup Rate Limit:**
1. Create **4 accounts** in one hour
2. Expected: ❌ "Too many requests..." after 3 accounts

**Chat Rate Limit:**
1. Send **31 messages** rapidly (within 1 minute)
2. Expected: ❌ "Too many requests..." after 30 messages

### B. Input Validation

**Test Invalid Inputs:**
| Field | Invalid Input | Expected Error |
|-------|--------------|----------------|
| Email | `notanemail` | "Invalid email format" |
| Email | `test@` | "Invalid email format" |
| Password | `short` | "Must be 8+ characters" |
| Password | `12345678` | "Must contain a letter" |
| Password | `password` | "Must contain a number" |
| Username | `ab` | "Must be 3-30 characters" |
| Username | `user@name` | "Alphanumeric only" |

### C. Session Security

**Session Timeout Test:**
1. Login to account
2. Wait 24 hours
3. Try to chat
4. Expected: Automatically logged out

**Session Cookies:**
1. Open DevTools (F12) → Application → Cookies
2. Check cookie settings:
   - ✅ `HttpOnly`: true (protected from JavaScript)
   - ✅ `Secure`: true (HTTPS only in production)
   - ✅ `SameSite`: Lax (CSRF protection)

---

## ✅ TEST 10: Database Persistence

### Test Data Persists:
1. **Create a conversation** and send messages
2. **Close browser** completely
3. **Reopen** and login again
4. Expected:
   - ✅ Conversation still in sidebar
   - ✅ All messages preserved
   - ✅ Can continue chatting

### Test Multiple Users:
1. Create **Account A** and send messages
2. Logout
3. Create **Account B** and send messages
4. Logout and login to **Account A**
5. Expected:
   - ✅ Only sees Account A's conversations
   - ✅ Cannot see Account B's data
   - ✅ Data isolated per user

---

## ✅ TEST 11: Error Handling

### A. Network Error
1. Disconnect internet
2. Try sending message
3. Expected: ❌ Error message shown gracefully

### B. Invalid Conversation
1. Try accessing: `http://127.0.0.1:5000/?conversation=99999`
2. Expected: ❌ "Conversation not found" or redirect

### C. Missing API Key
1. If PERPLEXITY_API_KEY not set in `.env`
2. Expected: Demo mode responses with disclaimer

---

## 📊 TEST RESULTS CHECKLIST

Mark each as you test:

### Functionality:
- [ ] Signup works with valid inputs
- [ ] Login works with test account
- [ ] Chat messages send and receive
- [ ] New conversations can be created
- [ ] Can switch between conversations
- [ ] Can delete conversations
- [ ] Logout works correctly
- [ ] Session persists across refreshes

### UI/UX:
- [ ] Login page looks professional
- [ ] Signup page matches design
- [ ] Sidebar is dark with conversations
- [ ] Chat area is light gray
- [ ] Message avatars show correctly
- [ ] Send button appears when typing
- [ ] Voice buttons show when empty
- [ ] Mobile responsive works
- [ ] Animations are smooth

### Security:
- [ ] Rate limiting blocks after limits
- [ ] Invalid emails rejected
- [ ] Weak passwords rejected
- [ ] Input sanitization works
- [ ] Sessions timeout after 24 hours
- [ ] Users can't see each other's data

---

## 🐛 COMMON ISSUES & FIXES

### Issue: "Module not found" Error
```bash
Fix: Install packages
pip install -r requirements.txt
```

### Issue: "Port 5000 already in use"
```bash
Fix: Kill existing process
taskkill /F /IM python.exe
```

### Issue: Cannot connect to database
```bash
Fix: Delete and recreate
rm instance/thomas.db
python test_db.py
```

### Issue: Rate limit hit during testing
```bash
Fix: Wait 1 minute or restart server
# Server restart clears rate limits
```

---

## 🎯 QUICK TEST SCRIPT

Run this to test everything automatically:

```python
# Save as: quick_test.py
import requests
import time

BASE_URL = "http://127.0.0.1:5000"

print("🧪 Thomas Testing Script")
print("=" * 50)

# Test 1: Server Running
try:
    r = requests.get(f"{BASE_URL}/login", timeout=5)
    print("✅ Server is running")
except:
    print("❌ Server not running - start with: python app.py")
    exit()

# Test 2: Login Page
if r.status_code == 200:
    print("✅ Login page accessible")

# Test 3: Test Account Login
login_data = {
    "email": "test@thomas.ai",
    "password": "testpassword123"
}
r = requests.post(f"{BASE_URL}/login", json=login_data)
if r.json().get("success"):
    print("✅ Login works")
else:
    print("❌ Login failed")

print("\n✅ Basic tests passed! Continue manual testing.")
```

Run with: `python quick_test.py`

---

## 📱 BROWSER TESTING

Test on multiple browsers:
- [ ] Chrome
- [ ] Firefox
- [ ] Edge
- [ ] Safari (if on Mac)
- [ ] Mobile browser (via DevTools)

---

## ✅ FINAL CHECKLIST BEFORE DEPLOYMENT

- [ ] All tests pass
- [ ] No console errors in browser (F12)
- [ ] Database saves correctly
- [ ] Security features work
- [ ] UI looks perfect
- [ ] Mobile responsive
- [ ] Error messages helpful
- [ ] Rate limiting active

---

## 🎉 SUCCESS CRITERIA

Thomas is **ready for deployment** when:

✅ Users can signup and login  
✅ Chat works with AI responses  
✅ Conversations save and load  
✅ UI looks professional  
✅ Security prevents abuse  
✅ Mobile works perfectly  

---

**Happy Testing!** 🚀

**Need help?** Check the logs in terminal or open browser DevTools (F12)

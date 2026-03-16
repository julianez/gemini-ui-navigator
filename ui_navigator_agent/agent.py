import os
import threading
import queue
import time
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
import pyautogui
from google.cloud import storage
from google.adk.agents import Agent
from google.genai import types

load_dotenv()
MODEL_ID = "gemini-3.1-flash-lite-preview"

# --- 1. CORE ENGINE (Threaded for Concurrency) ---
class PlaywrightWorker(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.task_queue = queue.Queue()
        self.result_queue = queue.Queue()

    def run(self):
        with sync_playwright() as p:
            try:
                browser = p.chromium.connect_over_cdp("http://localhost:9222")
                contexts = browser.contexts
                context = contexts[0] if contexts else browser.new_context()
                page = context.new_page()
                page.bring_to_front()
                
                while True:
                    task, args = self.task_queue.get()
                    
                    if task == "goto":
                        page.bring_to_front()
                        page.goto(args[0])
                        self.result_queue.put("✅ Chrome is ready.")

                    elif task == "visual_search":
                        page.bring_to_front()
                        time.sleep(1)
                        
                        # Safety click to focus Chrome
                        print("Safety click at top-left corner...")
                        pyautogui.click(100, 150)
                        time.sleep(0.5) 
                        
                        # Open Quick Search (Figma Shortcut)
                        pyautogui.hotkey('ctrl', 'alt', 'o')
                        time.sleep(1.5)
                        
                        # Type project name
                        print(f"Ghost keyboard typing: {args[0]}")
                        pyautogui.write(args[0], interval=0.15)
                        time.sleep(1.5) 
                        
                        # Navigate to gallery results
                        print("Pressing Enter to view search results...")
                        pyautogui.press('enter')
                        time.sleep(4.0) 
                        
                        # Click first result (Calibrated coordinates for split-screen)
                        screen_width, screen_height = pyautogui.size()
                        target_x = screen_width * 0.22 
                        target_y = screen_height * 0.20 
                        
                        print(f"Target locked! Moving mouse to X:{target_x}, Y:{target_y}...")
                        pyautogui.moveTo(target_x, target_y, duration=1.0, tween=pyautogui.easeInOutQuad)
                        pyautogui.doubleClick()
                        
                        # Move mouse slightly down to clear view
                        pyautogui.move(0, 100, duration=0.5) 
                        
                        print("Waiting 7 seconds for Figma canvas to load...")
                        time.sleep(7) 
                        
                        # STAGE 7: Canvas Activation & Zoom
                        print(">>> Focusing Web Canvas with Playwright Sniper Click <<<")
                        page.bring_to_front()
                        
                        viewport = page.viewport_size
                        if viewport:
                            page.mouse.click(viewport["width"] / 2, viewport["height"] / 2)
                        time.sleep(0.5) 
                        
                        print(">>> CLEARING SELECTION (ESC) <<<")
                        page.keyboard.press('Escape') 
                        time.sleep(0.5)
                        
                        print(">>> SELECTING FIRST FRAME (Key: N) <<<")
                        page.keyboard.press('n') 
                        time.sleep(1.5)
                        
                        # STAGE 8: Minimize UI for Clean Screenshot
                        print(">>> MINIMIZING FIGMA UI (Ctrl+Shift+|) <<<")
                        try:
                            btn_minimize = page.get_by_label("Minimize UI", exact=False).first

                            if not btn_minimize.is_visible():
                                btn_minimize = page.locator('button[data-testid="target-button"]').first

                            box = btn_minimize.bounding_box()
                            if box:
                                page.mouse.click(box['x'] + box['width']/2, box['y'] + box['height']/2)
                                time.sleep(2.5) 
                            else:
                                print("Didn't find button")
                        except Exception as e:
                            print(f"UI Minimization failed: {e}")
                        
                        time.sleep(1.5)
                        self.result_queue.put(f"✅ Project '{args[0]}' opened and UI minimized for capture.")

                    elif task == "screenshot":
                        page.bring_to_front()
                        image_bytes = page.screenshot()
                        part = types.Part(inline_data=types.Blob(mime_type='image/png', data=image_bytes))
                        self.result_queue.put(part)

            except Exception as e:
                self.result_queue.put(f"❌ Critical Error: {str(e)}")

pw_worker = PlaywrightWorker()
pw_worker.start()

# --- 2. AGENT TOOLS ---
def connect_to_chrome(url: str = "https://www.figma.com"):
    """Starts the Figma session."""
    pw_worker.task_queue.put(("goto", [url]))
    return pw_worker.result_queue.get()

def open_project_visually(project_name: str):
    """Searches and opens a project by moving the mouse and keyboard physically."""
    pw_worker.task_queue.put(("visual_search", [project_name]))
    return pw_worker.result_queue.get()

def take_screenshot():
    """Takes a screenshot, saves it for debugging, and sends it to the agent."""
    pw_worker.task_queue.put(("screenshot", []))
    part = pw_worker.result_queue.get()
    
    try:
        image_bytes = part.inline_data.data
        with open("debug_figma.png", "wb") as f:
            f.write(image_bytes)
        print("📸 Debug screenshot saved as 'debug_figma.png'")
    except Exception as e:
        print(f"⚠️ Error saving debug screenshot: {e}")
    
    return part

def save_generated_code(code: str, filename: str = "App.tsx"):
    """Saves the React Native code generated by the agent into a physical file."""
    if code.startswith("```"):
        lines = code.split("\n")
        if len(lines) > 2:
            code = "\n".join(lines[1:-1])
            
    filepath = os.path.join(os.getcwd(), filename)
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(code)
        return f"✅ Physical file '{filename}' created successfully."
    except Exception as e:
        return f"❌ OS Error saving file: {str(e)}"

def upload_to_gcs(content: str, filename: str = "GeminiChallenge.tsx"):

    PROJECT_ID = "gem-challenge-julianez" 
    BUCKET_NAME = "bucket_gem_challenge"
    print(">>> Uploading Code to GCS Bucket <<<")

    try:
        storage_client = storage.Client(project=PROJECT_ID)
        bucket = storage_client.bucket(BUCKET_NAME)
        
        blob = bucket.blob(filename)
        blob.upload_from_string(content, content_type='text/plain')
        
        public_url = f"https://storage.googleapis.com/{BUCKET_NAME}/{filename}"

        print(f"✅ File Uploaded to Cloud {public_url}")

        return f"✅ Uploaded to Cloud: {public_url}"
    except Exception as e:
        return f"❌ Cloud Storage Error: {str(e)}"

# --- 3. THE BRAIN (System Instruction) ---
root_agent = Agent(
    name="UI_Navigator_Agent",
    model=MODEL_ID,
    instruction="""
    You are a high-precision UI Navigator and React Native Expert. 
    Your ONLY source of truth is the provided image. DO NOT use prior knowledge of banking apps.

    STEP 1: Greet the user and ask: "Which Figma project would you like me to open?". (Wait for response)
    STEP 2: Use 'connect_to_chrome', then 'open_project_visually' with the name provided.
    STEP 3: Once opened, use 'take_screenshot' EXACTLY once.
    STEP 4: 
    1. VISUAL SCAN: Identify exact text (e.g., 'Hola Maria José', 'USD: $950', 'Transferir ahora').
    2. COLOR EXTRACTION: Use a visual color picker logic on the image to get hex codes for the dark background and primary buttons.
    3. FAITHFUL CODING: 
       - Generate React Native code reflecting the exact visual hierarchy.
       - Use 'SafeAreaView', 'StatusBar', 'TouchableOpacity', and 'StyleSheet'.
       - Use accurate corporate colors (Scotiabank Red, Dark Grey, White).
    4. STORAGE:
        - FIRST: Use 'save_generated_code' for local persistence.
        - SECOND: Use 'upload_to_gcs' to persist the code in Google Cloud.
        - FINAL: Provide the public URL to the user and say goodbye. 
    """,
    tools=[connect_to_chrome, open_project_visually, take_screenshot, save_generated_code,upload_to_gcs]
)
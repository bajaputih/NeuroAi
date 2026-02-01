#!/usr/bin/env python3
# Neuro Ai System v3.0 - Full Streaming Mode
# Creator: azfla
# Powered by OpenRouter.ai

import os
import sys
import requests
import json
import time
from datetime import datetime
import readline
import threading

# Fungsi untuk clear screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Fungsi untuk display banner
def display_banner():
    clear_screen()
    banner = '''
\033[91m
███╗   ██╗███████╗██╗   ██╗██████╗  ██████╗      █████╗ ██╗
████╗  ██║██╔════╝██║   ██║██╔══██╗██╔═══██╗    ██╔══██╗██║
██╔██╗ ██║█████╗  ██║   ██║██████╔╝██║   ██║    ███████║██║
██║╚██╗██║██╔══╝  ██║   ██║██╔══██╗██║   ██║    ██╔══██║██║
██║ ╚████║███████╗╚██████╔╝██║  ██║╚██████╔╝    ██║  ██║██║
╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝     ╚═╝  ╚═╝╚═╝
\033[0m
    '''
    print(banner)
    print("\033[93m" + "="*60 + "\033[0m")
    print("\033[92m" + "Neuro Ai System v3.0" + "\033[0m")
    print("\033[96m" + "Creator: azfla" + "\033[0m")
    print("\033[95m" + "Powered by OpenRouter.ai | Full Streaming Mode" + "\033[0m")
    print("\033[93m" + "="*60 + "\033[0m")
    print()

# Daftar model yang tersedia
AVAILABLE_MODELS = {
    "1": {
        "id": "meta-llama/llama-3.3-70b-instruct",
        "name": "Llama 3.3 70B",
        "provider": "Meta",
        "context": 128000,
        "description": "Model terbaru dari Meta, sangat baik untuk berbagai tugas"
    },
    "2": {
        "id": "mistralai/mistral-7b-instruct",
        "name": "Mistral 7B",
        "provider": "Mistral AI",
        "context": 32768,
        "description": "Model ringan dan efisien dari Mistral AI"
    },
    "3": {
        "id": "google/gemini-2.0-flash-exp:free",
        "name": "Gemini 2.0 Flash",
        "provider": "Google",
        "context": 8192,
        "description": "Model cepat dari Google, gratis untuk penggunaan terbatas"
    },
    "4": {
        "id": "anthropic/claude-3.5-haiku",
        "name": "Claude 3.5 Haiku",
        "provider": "Anthropic",
        "context": 200000,
        "description": "Model cepat dari Anthropic, sangat baik untuk kreativitas"
    },
    "5": {
        "id": "qwen/qwen-2.5-72b-instruct",
        "name": "Qwen 2.5 72B",
        "provider": "Alibaba",
        "context": 32768,
        "description": "Model open-source besar dari Alibaba"
    },
    "6": {
        "id": "microsoft/phi-3.5-mini-instruct",
        "name": "Phi-3.5 Mini",
        "provider": "Microsoft",
        "context": 4096,
        "description": "Model kecil tapi powerful dari Microsoft"
    }
}

# Fungsi untuk validasi API key
def validate_api_key(api_key):
    """Validasi API key dengan test request"""
    if not api_key or not api_key.startswith("sk-or-v1-"):
        return False
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://neuro-ai.azfla",
        "X-Title": "Neuro Ai System"
    }
    
    test_payload = {
        "model": "meta-llama/llama-3.1-8b-instruct",
        "messages": [{"role": "user", "content": "test"}],
        "max_tokens": 5,
        "stream": True
    }
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=test_payload,
            timeout=10
        )
        return response.status_code == 200
    except Exception:
        return False

# Fungsi untuk mendapatkan API key dari user
def get_api_key():
    display_banner()
    print("\033[96m" + "API KEY SETUP" + "\033[0m")
    print("\033[90m" + "="*60 + "\033[0m")
    print("\033[93m1. Buka website: https://openrouter.ai/")
    print("2. Buat akun atau login")
    print("3. Klik 'Get API Key' di dashboard")
    print("4. Copy API key Anda (dimulai dengan sk-or-v1-)")
    print("5. Masukkan API key di bawah ini\033[0m")
    print("\033[90m" + "="*60 + "\033[0m\n")
    
    attempts = 3
    while attempts > 0:
        api_key = input("\033[94mMasukkan API Key OpenRouter: \033[0m").strip()
        
        if not api_key:
            print("\033[91mAPI key tidak boleh kosong!\033[0m")
            attempts -= 1
            if attempts > 0:
                print(f"\033[93mSisa percobaan: {attempts}\033[0m")
            continue
            
        print("\033[93mMemvalidasi API key...\033[0m")
        
        if validate_api_key(api_key):
            print("\033[92m✓ API key valid!\033[0m")
            time.sleep(1)
            return api_key
        else:
            attempts -= 1
            if attempts > 0:
                print(f"\033[91m✗ API key tidak valid. Sisa percobaan: {attempts}\033[0m")
            else:
                print("\033[91m✗ Gagal validasi API key.\033[0m")
                print("\033[93mPastikan:")
                print("1. API key benar (dimulai dengan sk-or-v1-)")
                print("2. Koneksi internet stabil")
                print("3. Saldo API key mencukupi")
                print("\033[0m")
                sys.exit(1)
    
    return None

# Fungsi untuk memilih model
def select_model():
    clear_screen()
    display_banner()
    print("\033[96m" + "PILIH MODEL AI" + "\033[0m")
    print("\033[90m" + "="*60 + "\033[0m")
    print("\033[93mPilih model yang ingin digunakan:\033[0m\n")
    
    for key, model in AVAILABLE_MODELS.items():
        print(f"\033[92m[{key}] {model['name']}")
        print(f"   Provider: {model['provider']}")
        print(f"   Context: {model['context']:,} tokens")
        print(f"   Deskripsi: {model['description']}\033[0m\n")
    
    while True:
        choice = input("\033[94mPilih model [1-6]: \033[0m").strip()
        
        if choice in AVAILABLE_MODELS:
            selected_model = AVAILABLE_MODELS[choice]
            print(f"\033[92m✓ Model dipilih: {selected_model['name']}\033[0m")
            time.sleep(1)
            return selected_model
        else:
            print("\033[91mPilihan tidak valid! Harap pilih angka 1-6.\033[0m")

# Class untuk Full Streaming Neuro AI
class FullStreamNeuroAi:
    def __init__(self, api_key, model_info):
        self.api_key = api_key
        self.model_id = model_info["id"]
        self.model_name = model_info["name"]
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://neuro-ai.azfla",
            "X-Title": "Neuro Ai System"
        }
        self.conversation_history = []
        
    def get_system_prompt(self):
        """System prompt untuk AI assistant"""
        return """ANDA ADALAH NEURO AI - ASSISTANT AI YANG SANGAT MEMBANTU.
        
TUGAS ANDA:
1. Bantu pengguna dengan informasi yang akurat dan bermanfaat
2. Berikan penjelasan yang jelas dan mudah dimengerti
3. Tawarkan solusi yang praktis dan dapat diimplementasikan
4. Jadilah ramah, sopan, dan profesional
5. Fokus pada memberikan nilai tambah kepada pengguna

PRINSIP:
- Jawab pertanyaan dengan informasi faktual
- Akui ketika tidak tahu sesuatu
- Tawarkan alternatif atau sumber informasi lain

FORMAT RESPONS:
- Berikan jawaban yang terstruktur
- Gunakan poin-poin jika perlu
- Jelaskan dengan bahasa yang mudah dipahami"""
    
    def stream_chat(self, message, display_prefix=True):
        """Stream chat dengan response real-time"""
        start_time = time.time()
        
        # Tambahkan user message ke history
        self.conversation_history.append({"role": "user", "content": message})
        
        # Siapkan messages untuk API
        messages = [
            {"role": "system", "content": self.get_system_prompt()}
        ]
        
        # Tambahkan conversation history (maksimal 10 pesan terakhir)
        history_to_send = self.conversation_history[-10:] if len(self.conversation_history) > 10 else self.conversation_history
        messages.extend(history_to_send)
        
        payload = {
            "model": self.model_id,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 4000,
            "top_p": 0.9,
            "stream": True
        }
        
        try:
            if display_prefix:
                print(f"\033[90m[Model: {self.model_name}]\033[0m")
                print("\033[92mNeuro Ai:\033[0m ", end="", flush=True)
            
            full_response = ""
            
            # Kirim request dengan streaming
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=self.headers,
                json=payload,
                stream=True,
                timeout=60
            )
            
            # Proses streaming response
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        data = line[6:]
                        if data != '[DONE]':
                            try:
                                json_data = json.loads(data)
                                if 'choices' in json_data and len(json_data['choices']) > 0:
                                    delta = json_data['choices'][0].get('delta', {})
                                    if 'content' in delta:
                                        content = delta['content']
                                        print(content, end="", flush=True)
                                        full_response += content
                            except json.JSONDecodeError:
                                continue
                            except Exception as e:
                                print(f"\033[91m\nError parsing: {str(e)[:100]}\033[0m")
                                continue
            
            # Hitung waktu respons
            elapsed_time = time.time() - start_time
            
            print()  # New line setelah stream selesai
            
            # Tambahkan AI response ke history
            if full_response:
                self.conversation_history.append({"role": "assistant", "content": full_response})
            
            # Tampilkan info waktu
            print(f"\033[90m[Response time: {elapsed_time:.2f}s]\033[0m")
            
            return full_response
            
        except requests.exceptions.Timeout:
            print("\033[91m\n✗ Timeout: Server tidak merespons\033[0m")
            return None
        except requests.exceptions.ConnectionError:
            print("\033[91m\n✗ Connection Error: Tidak dapat terhubung ke server\033[0m")
            return None
        except Exception as e:
            print(f"\033[91m\n✗ Error: {str(e)}\033[0m")
            return None
    
    def clear_history(self):
        """Hapus conversation history"""
        self.conversation_history = []
        return True

# Fungsi untuk display menu utama
def display_main_menu(neuro_ai):
    clear_screen()
    display_banner()
    
    # Tampilkan info model yang sedang digunakan
    print("\033[96m" + "CURRENT MODEL" + "\033[0m")
    print("\033[90m" + "="*60 + "\033[0m")
    print(f"\033[92m• Model:\033[0m {neuro_ai.model_name}")
    print(f"\033[92m• Provider:\033[0m {AVAILABLE_MODELS[[k for k, v in AVAILABLE_MODELS.items() if v['id'] == neuro_ai.model_id][0]]['provider']}")
    print(f"\033[92m• Context:\033[0m {AVAILABLE_MODELS[[k for k, v in AVAILABLE_MODELS.items() if v['id'] == neuro_ai.model_id][0]]['context']:,} tokens")
    print(f"\033[92m• History:\033[0m {len(neuro_ai.conversation_history)} messages")
    print("\033[90m" + "="*60 + "\033[0m")
    
    print("\n\033[96m" + "MAIN MENU - FULL STREAMING MODE" + "\033[0m")
    print("\033[93m" + "="*60 + "\033[0m")
    print("\033[92m[1]\033[0m Start Chat Session")
    print("\033[92m[2]\033[0m View Chat History")
    print("\033[92m[3]\033[0m Change AI Model")
    print("\033[92m[4]\033[0m Change API Key")
    print("\033[92m[5]\033[0m Clear Chat History")
    print("\033[92m[6]\033[0m System Information")
    print("\033[92m[7]\033[0m Exit Program")
    print("\033[93m" + "="*60 + "\033[0m")

# Fungsi untuk chat session dengan full streaming
def chat_session(neuro_ai):
    clear_screen()
    display_banner()
    
    print("\033[96m" + "CHAT SESSION - REAL-TIME STREAMING" + "\033[0m")
    print("\033[90m" + "="*60 + "\033[0m")
    print(f"\033[93mModel: {neuro_ai.model_name}\033[0m")
    print("\033[93mType your message. Type '/back' to return to menu.")
    print("Type '/clear' to clear screen.")
    print("Type '/help' for commands list.")
    print("\033[0m")
    print("\033[90m" + "="*60 + "\033[0m")
    print("\033[92mAI will respond in real-time as it types...\033[0m\n")
    
    message_count = 0
    
    while True:
        try:
            # Input user dengan warna berbeda
            user_input = input("\n\033[95mYou: \033[0m").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.lower() in ['/back', '/exit', '/quit']:
                print("\033[93mReturning to main menu...\033[0m")
                time.sleep(1)
                break
            
            elif user_input.lower() == '/clear':
                clear_screen()
                display_banner()
                print("\033[96m" + "CHAT SESSION - REAL-TIME STREAMING" + "\033[0m")
                print("\033[90m" + "="*60 + "\033[0m")
                print(f"\033[93mModel: {neuro_ai.model_name}\033[0m")
                print("\033[93mChat continues...\033[0m")
                continue
            
            elif user_input.lower() == '/help':
                print("\033[94mAvailable Commands:")
                print("  /back    - Return to main menu")
                print("  /clear   - Clear the screen")
                print("  /help    - Show this help")
                print("  /model   - Show current model info")
                print("  /history - Show message count")
                print("\033[0m")
                continue
            
            elif user_input.lower() == '/model':
                print(f"\033[94mCurrent Model: {neuro_ai.model_name}")
                print(f"Model ID: {neuro_ai.model_id}")
                print(f"Messages in session: {len(neuro_ai.conversation_history)}\033[0m")
                continue
            
            elif user_input.lower() == '/history':
                print(f"\033[94mTotal messages in conversation: {len(neuro_ai.conversation_history)}")
                print(f"User messages: {len([m for m in neuro_ai.conversation_history if m['role'] == 'user'])}")
                print(f"AI responses: {len([m for m in neuro_ai.conversation_history if m['role'] == 'assistant'])}\033[0m")
                continue
            
            # Process chat with streaming
            message_count += 1
            print(f"\033[90m[Message #{message_count}]\033[0m")
            neuro_ai.stream_chat(user_input)
            
        except KeyboardInterrupt:
            print("\n\033[93m\nInterrupt detected. Returning to menu...\033[0m")
            time.sleep(1)
            break
        except Exception as e:
            print(f"\033[91mError: {str(e)}\033[0m")

# Fungsi untuk melihat history
def view_history(neuro_ai):
    clear_screen()
    display_banner()
    print("\033[96m" + "CHAT HISTORY" + "\033[0m")
    print("\033[90m" + "="*60 + "\033[0m")
    print(f"\033[94mModel: {neuro_ai.model_name}\033[0m")
    print(f"\033[94mTotal conversations: {len(neuro_ai.conversation_history)} messages\033[0m")
    
    if not neuro_ai.conversation_history:
        print("\033[93mNo chat history yet.\033[0m")
    else:
        print("\033[90m" + "-"*60 + "\033[0m")
        
        # Tampilkan dalam format yang lebih baik
        for i, msg in enumerate(neuro_ai.conversation_history, 1):
            role = "You" if msg["role"] == "user" else "Neuro Ai"
            timestamp = datetime.now().strftime('%H:%M:%S')
            color = "\033[95m" if msg["role"] == "user" else "\033[92m"
            
            print(f"{color}[{timestamp}] {role}:\033[0m")
            
            # Tampilkan isi pesan dengan wrapping
            content = msg['content']
            # Split content menjadi lines setiap 70 karakter
            lines = [content[j:j+70] for j in range(0, len(content), 70)]
            for line in lines:
                print(f"  {line}")
            print()
    
    print("\033[90m" + "="*60 + "\033[0m")
    input("\n\033[90mPress Enter to continue...\033[0m")

# Fungsi untuk system info
def system_info(neuro_ai):
    clear_screen()
    display_banner()
    print("\033[96m" + "SYSTEM INFORMATION" + "\033[0m")
    print("\033[90m" + "="*60 + "\033[0m")
    
    info_items = [
        ("System Name", "Neuro Ai v3.0"),
        ("Creator", "azfla"),
        ("Mode", "Full Streaming"),
        ("Current Model", neuro_ai.model_name),
        ("Model ID", neuro_ai.model_id),
        ("API Provider", "OpenRouter.ai"),
        ("Status", "Connected ✓"),
        ("Chat History", f"{len(neuro_ai.conversation_history)} messages"),
        ("Active Since", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        ("Python Version", f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    ]
    
    for label, value in info_items:
        print(f"\033[92m{label:20}\033[0m: {value}")
    
    print("\033[90m" + "="*60 + "\033[0m")
    
    # Tampilkan semua model yang tersedia
    print("\n\033[96m" + "AVAILABLE MODELS" + "\033[0m")
    print("\033[90m" + "-"*60 + "\033[0m")
    for key, model in AVAILABLE_MODELS.items():
        status = "✓ CURRENT" if model["id"] == neuro_ai.model_id else "○ Available"
        color = "\033[92m" if model["id"] == neuro_ai.model_id else "\033[93m"
        print(f"{color}[{key}] {status} - {model['name']} ({model['provider']})\033[0m")
    
    print("\033[90m" + "="*60 + "\033[0m")
    input("\n\033[90mPress Enter to continue...\033[0m")

# Fungsi utama
def main():
    # Cek dependencies
    try:
        import requests
    except ImportError:
        print("\033[91mError: Package 'requests' tidak terinstall!\033[0m")
        print("\033[93mInstall dengan: pip install requests\033[0m")
        sys.exit(1)
    
    # Setup readline untuk history
    readline.parse_and_bind("tab: complete")
    readline.set_history_length(100)
    
    # Langkah 1: Dapatkan API key
    api_key = get_api_key()
    if not api_key:
        print("\033[91mFailed to get valid API key.\033[0m")
        sys.exit(1)
    
    # Langkah 2: Pilih model
    model_info = select_model()
    
    # Inisialisasi Neuro Ai dengan model yang dipilih
    neuro_ai = FullStreamNeuroAi(api_key, model_info)
    
    print("\033[92m✓ Neuro Ai System initialized successfully!\033[0m")
    print(f"\033[92m✓ Model: {neuro_ai.model_name}\033[0m")
    print(f"\033[92m✓ Mode: Full Real-time Streaming\033[0m")
    time.sleep(2)
    
    # Main loop
    while True:
        display_main_menu(neuro_ai)
        
        try:
            choice = input("\n\033[94mSelect menu [1-7]: \033[0m").strip()
            
            if choice == "1":
                chat_session(neuro_ai)
            elif choice == "2":
                view_history(neuro_ai)
            elif choice == "3":
                # Change model
                model_info = select_model()
                neuro_ai = FullStreamNeuroAi(api_key, model_info)
                print(f"\033[92m✓ Model changed to: {neuro_ai.model_name}\033[0m")
                time.sleep(2)
            elif choice == "4":
                # Change API key
                clear_screen()
                display_banner()
                print("\033[96m" + "CHANGE API KEY" + "\033[0m")
                print("\033[90m" + "="*60 + "\033[0m")
                new_api_key = input("\033[94mEnter new API key: \033[0m").strip()
                
                if validate_api_key(new_api_key):
                    neuro_ai.api_key = new_api_key
                    neuro_ai.headers["Authorization"] = f"Bearer {new_api_key}"
                    api_key = new_api_key
                    print("\033[92m✓ API key changed successfully.\033[0m")
                else:
                    print("\033[91m✗ Invalid API key.\033[0m")
                time.sleep(2)
            elif choice == "5":
                # Clear history
                neuro_ai.clear_history()
                print("\033[92m✓ Chat history cleared.\033[0m")
                time.sleep(1)
            elif choice == "6":
                system_info(neuro_ai)
            elif choice == "7":
                print("\n\033[92mThank you for using Neuro Ai!\033[0m")
                print("\033[96mCreator: azfla | System: Neuro Ai v3.0\033[0m")
                time.sleep(2)
                break
            else:
                print("\033[91mInvalid selection! Please choose 1-7.\033[0m")
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n\n\033[93mInterrupt detected. Exiting...\033[0m")
            time.sleep(1)
            break
        except Exception as e:
            print(f"\033[91mError: {str(e)}\033[0m")
            time.sleep(2)

# Entry point
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\033[93mProgram terminated by user.\033[0m")
    except Exception as e:
        print(f"\033[91mFatal error: {str(e)}\033[0m")
        sys.exit(1)
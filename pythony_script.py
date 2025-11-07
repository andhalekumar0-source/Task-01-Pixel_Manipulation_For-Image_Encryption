import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os

# --- Encryption/Decryption Logic ---
def simple_xor_cipher(image_path, output_path, key=123):
    """
    Encrypts or Decrypts an image using a simple XOR operation on pixel values.
    """
    try:
        img = Image.open(image_path)
        img = img.convert("RGB")
        width, height = img.size
        pixels = img.load()
        
        new_img = Image.new('RGB', (width, height))
        new_pixels = new_img.load()
        
        # Iterate over each pixel and apply XOR
        for i in range(width):
            for j in range(height):
                r, g, b = pixels[i, j]
                r_new = r ^ key
                g_new = g ^ key
                b_new = b ^ key
                new_pixels[i, j] = (r_new, g_new, b_new)

        new_img.save(output_path)
        return True, f"Image successfully processed and saved to: {output_path}"
    
    except FileNotFoundError:
        return False, "Error: File not found."
    except Exception as e:
        return False, f"An error occurred: {e}"

# --- Tkinter GUI Implementation ---
class ImageCipherApp:
    def __init__(self, master):  # ✅ Fixed here
        self.master = master
        master.title("Simple Image Cipher Tool")
        master.geometry("400x300")
        
        self.file_path = None
        self.key = 123  # Fixed key for simplicity

        # 1. File Selection
        self.label_file = tk.Label(master, text="No file selected.")
        self.label_file.pack(pady=10)

        self.btn_select = tk.Button(master, text="Select Image", command=self.select_image)
        self.btn_select.pack(pady=5)
        
        tk.Frame(master, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx=10, pady=10)

        # 2. Key Info
        self.label_key = tk.Label(master, text=f"Fixed XOR Key: {self.key}\n(Encryption and Decryption use the same key.)")
        self.label_key.pack(pady=5)

        # 3. Operation Buttons
        self.btn_encrypt = tk.Button(master, text="Encrypt Image", command=self.encrypt_image, bg="#4CAF50", fg="white")
        self.btn_encrypt.pack(pady=10)

        self.btn_decrypt = tk.Button(master, text="Decrypt Image", command=self.decrypt_image, bg="#2196F3", fg="white")
        self.btn_decrypt.pack(pady=5)

    def select_image(self):
        self.file_path = filedialog.askopenfilename(
            defaultextension=".png",
            filetypes=[("Image files", ".png;.jpg;.jpeg;.bmp")]
        )
        if self.file_path:
            self.label_file.config(text=f"Selected: {os.path.basename(self.file_path)}")
        else:
            self.label_file.config(text="No file selected.")

    def process_image(self, operation):
        if not self.file_path:
            messagebox.showerror("Error", "Please select an image first.")
            return

        base, ext = os.path.splitext(self.file_path)
        if operation == "Encrypt":
            output_path = base + "_encrypted" + ext
        else:
            output_path = base + "_decrypted" + ext
            
        save_path = filedialog.asksaveasfilename(
            defaultextension=ext,
            initialfile=os.path.basename(output_path),
            filetypes=[("Image files", f"*{ext}")]
        )

        if save_path:
            success, message = simple_xor_cipher(self.file_path, save_path, self.key)
            if success:
                messagebox.showinfo(f"{operation} Complete", message)
            else:
                messagebox.showerror(f"{operation} Failed", message)

    def encrypt_image(self):
        self.process_image("Encrypt")

    def decrypt_image(self):
        self.process_image("Decrypt")


# --- Main Execution Block ---
if __name__ == "__main__":  # ✅ Fixed here
    try:
        root = tk.Tk()
        app = ImageCipherApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Error during application startup: {e}")
        print("Make sure Tkinter (built-in) and Pillow (pip install Pillow) are installed.")

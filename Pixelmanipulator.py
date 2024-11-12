import os
from tkinter import Tk, Button, Label, Entry, filedialog, messagebox
from PIL import Image
import random

def get_seeded_random(seed):
    """Returns a seeded random generator."""
    return random.Random(seed)

def encrypt_image(input_image_path, output_image_path, seed):
    """Encrypts the image by manipulating pixel values."""
    image = Image.open(input_image_path)
    width, height = image.size
    pixels = list(image.getdata())
    random_gen = get_seeded_random(seed)

    
    indices = list(range(len(pixels)))
    random_gen.shuffle(indices)
    encrypted_pixels = [pixels[i] for i in indices]

    
    encrypted_image = Image.new(image.mode, (width, height))
    encrypted_image.putdata(encrypted_pixels)
    encrypted_image.save(output_image_path)
    
    return True

def decrypt_image(input_image_path, output_image_path, seed):
    """Decrypts the image by reversing the encryption process."""
    image = Image.open(input_image_path)
    width, height = image.size
    
    encrypted_pixels = list(image.getdata())
    random_gen = get_seeded_random(seed)

    
    indices = list(range(len(encrypted_pixels)))
    random_gen.shuffle(indices)

    
    decrypted_pixels = [None] * len(encrypted_pixels)

    
    for shuffled_index, original_index in enumerate(indices):
        decrypted_pixels[original_index] = encrypted_pixels[shuffled_index]

    
    decrypted_image = Image.new(image.mode, (width, height))
    decrypted_image.putdata(decrypted_pixels)
    decrypted_image.save(output_image_path)

    return True

def select_input_image():
    """Opens a file dialog to select an input image."""
    input_image_path = filedialog.askopenfilename(title="Select Image")
    input_image_label.config(text=input_image_path)

def select_output_image():
    """Opens a file dialog to select an output image path."""
    output_image_path = filedialog.asksaveasfilename(defaultextension=".png", 
        filetypes=[("PNG files", "*.png"),("JPEG files", "*.jpg;*.jpeg"),("All files", "*.*")], 
        title="Save Encrypted/Decrypted Image")
    output_image_label.config(text=output_image_path)

def encrypt():
    input_image_path = input_image_label.cget("text")
    output_image_path = output_image_label.cget("text")
    seed = seed_entry.get()

    if not input_image_path or not output_image_path:
        messagebox.showerror("Error", "Please select input and output images.")
        return

    if encrypt_image(input_image_path, output_image_path, seed):
        messagebox.showinfo("Success", "Image encrypted successfully!")

def decrypt():
    input_image_path = input_image_label.cget("text")
    output_image_path = output_image_label.cget("text")
    seed = seed_entry.get()

    if not input_image_path or not output_image_path:
        messagebox.showerror("Error", "Please select input and output images.")
        return

    if decrypt_image(input_image_path, output_image_path, seed):
        messagebox.showinfo("Success", "Image decrypted successfully!")

root = Tk()
root.title("Image Encryption Tool")


Label(root, text="Select Image to Encrypt/Decrypt:").pack(pady=5)
input_image_label = Label(root, text="No image selected")
input_image_label.pack(pady=5)

Button(root, text="Browse", command=select_input_image).pack(pady=5)

Label(root, text="Output Image Path:").pack(pady=5)
output_image_label = Label(root, text="No output path selected")
output_image_label.pack(pady=5)

Button(root, text="Save As", command=select_output_image).pack(pady=5)

Label(root, text="Enter Seed Key:").pack(pady=5)
seed_entry = Entry(root)
seed_entry.pack(pady=5)

Button(root, text="Encrypt Image", command=encrypt).pack(pady=5)
Button(root, text="Decrypt Image", command=decrypt).pack(pady=5)

root.mainloop()
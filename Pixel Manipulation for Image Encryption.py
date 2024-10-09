from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import os

# Function to perform diffusion on RGB values
def image_diffusion_rgb(img_array, key):
    height, width, channels = img_array.shape
    diffused_img = np.copy(img_array)
    
    for i in range(height):
        for j in range(width):
            for k in range(channels):  # For each RGB channel
                if i > 0 or j > 0:
                    prev_pixel = diffused_img[i-1, j, k] if j == 0 else diffused_img[i, j-1, k]
                    diffused_img[i, j, k] = (diffused_img[i, j, k] ^ prev_pixel ^ key) % 256
    return diffused_img

# Function to perform substitution on RGB values
def image_substitution_rgb(img_array, key):
    return (img_array + key) % 256

# Function to encrypt the image using diffusion-substitution on RGB channels
def encrypt_image_rgb(image_path, key):
    img = Image.open(image_path).convert('RGB')  # Convert to RGB
    img_array = np.array(img)
    
    # Step 1: Diffusion
    diffused_img = image_diffusion_rgb(img_array, key)
    
    # Step 2: Substitution
    encrypted_img_array = image_substitution_rgb(diffused_img, key)
    
    encrypted_img = Image.fromarray(encrypted_img_array.astype('uint8'))
    return encrypted_img

# Function to decrypt the image (reverse of encryption for RGB channels)
def decrypt_image_rgb(image_path, key):
    img = Image.open(image_path).convert('RGB')  # Convert to RGB
    img_array = np.array(img)
    
    # Reverse Step 2: Substitution (subtracting the key)
    substituted_img = (img_array - key) % 256
    
    # Reverse Step 1: Diffusion (same diffusion method but reversed)
    height, width, channels = substituted_img.shape
    decrypted_img = np.copy(substituted_img)
    for i in range(height - 1, -1, -1):
        for j in range(width - 1, -1, -1):
            for k in range(channels):  # For each RGB channel
                if i > 0 or j > 0:
                    prev_pixel = decrypted_img[i-1, j, k] if j == 0 else decrypted_img[i, j-1, k]
                    decrypted_img[i, j, k] = (decrypted_img[i, j, k] ^ prev_pixel ^ key) % 256
    
    decrypted_img = Image.fromarray(decrypted_img.astype('uint8'))
    return decrypted_img

# Function to browse image
def browse_image():
    global image_path
    image_path = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select an Image",
                                            filetypes=(("PNG files", "*.png"), ("JPG files", "*.jpg"), ("All files", "*.*")))
    if image_path:
        load_image(image_path)

# Function to load and display the image in the GUI
def load_image(path):
    img = Image.open(path).convert('RGB')
    img.thumbnail((200, 200))  # Resize image for display
    img = ImageTk.PhotoImage(img)
    img_label.config(image=img)
    img_label.image = img  # Save a reference to the image to prevent garbage collection

# Function to encrypt and save the image
def encrypt_and_save():
    try:
        key = int(shift_entry.get())  # Validate that key is an integer
        if image_path:
            encrypted_img = encrypt_image_rgb(image_path, key)
            save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
            if save_path:
                encrypted_img.save(save_path)
                messagebox.showinfo("Success", f"Encrypted image saved as {save_path}")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid numeric key.")

# Function to decrypt and save the image
def decrypt_and_save():
    try:
        key = int(shift_entry.get())  # Validate that key is an integer
        if image_path:
            decrypted_img = decrypt_image_rgb(image_path, key)
            save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
            if save_path:
                decrypted_img.save(save_path)
                messagebox.showinfo("Success", f"Decrypted image saved as {save_path}")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid numeric key.")

# Initialize the GUI window
root = Tk()
root.title("RGB Image Diffusion-Substitution Encryption")
root.geometry("600x600")  # Adjusted size to make it larger
root.configure(bg="lightgray")

# Widgets
Label(root, text="RGB Image Diffusion-Substitution Encryption", font=("Arial", 16), bg="lightgray").pack(pady=20)

# Image display label
img_label = Label(root)
img_label.pack(pady=10)

# Browse Button
browse_button = Button(root, text="Browse Image", command=browse_image, bg="blue", fg="white")
browse_button.pack(pady=10)

# Shift Key Label and Entry
Label(root, text="Enter Encryption Key (numeric):", bg="lightgray").pack()
shift_entry = Entry(root, width=15)
shift_entry.pack(pady=5)

# Encrypt and Decrypt Buttons
encrypt_button = Button(root, text="Encrypt Image", command=encrypt_and_save, bg="green", fg="white")
encrypt_button.pack(pady=10)

decrypt_button = Button(root, text="Decrypt Image", command=decrypt_and_save, bg="red", fg="white")
decrypt_button.pack(pady=10)

# Run the GUI main loop
root.mainloop()

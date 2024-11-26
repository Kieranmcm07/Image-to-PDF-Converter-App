import tkinter as tk
from tkinter import filedialog
from PIL import Image
from reportlab.pdfgen import canvas
import os


# Main function to start the application
def main():
    # Create the main window
    main_window = tk.Tk()
    main_window.title("Image to PDF")  # Set the title of the main window

    # Create an instance of the ImageToPDFConverter class
    image_converter = ImageToPDFConverter(main_window)

    # Set the size of the main window
    main_window.geometry("400x600")

    # Start the main event loop of the application
    main_window.mainloop()


# Class to convert images to PDF
class ImageToPDFConverter:
    # Constructor to initialize the converter
    def __init__(self, root):
        self.root = root  # Reference to the main window
        self.image_file_paths = []  # List to store the selected image file paths
        self.output_pdf_file_name = (
            tk.StringVar()
        )  # Variable to store the output PDF file name
        self.selected_images_listbox = tk.Listbox(
            root, selectmode=tk.MULTIPLE
        )  # Listbox to display the selected images

        # Initialize the UI components
        self.initialize_ui()

    # Method to initialize the UI components
    def initialize_ui(self):
        # Create a title label
        title_label = tk.Label(
            self.root, text="Image to PDF Converter", font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)  # Add the label to the window

        # Create a button to select images
        select_images_button = tk.Button(
            self.root, text="Select Images", command=self.select_images
        )
        select_images_button.pack(pady=(0, 10))  # Add the button to the window

        # Add the listbox to display the selected images
        self.selected_images_listbox.pack(pady=(0, 10), fill=tk.BOTH, expand=True)

        # Create a label and entry to input the output PDF file name
        label = tk.Label(self.root, text="Enter output PDF name:")
        label.pack()
        pdf_name_entry = tk.Entry(
            self.root,
            textvariable=self.output_pdf_file_name,
            width=40,
            justify="center",
        )
        pdf_name_entry.pack()

        # Create a button to convert the images to PDF
        convert_button = tk.Button(
            self.root, text="Convert to PDF", command=self.convert_images_to_pdf
        )
        convert_button.pack(pady=(20, 40))  # Add the button to the window

    # Method to select images
    def select_images(self):
        # Open a file dialog to select images
        self.image_file_paths = filedialog.askopenfilenames(
            title="Select Images", filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")]
        )

        # Update the listbox with the selected images
        self.update_selected_images_listbox()

    # Method to update the listbox with the selected images
    def update_selected_images_listbox(self):
        # Clear the listbox
        self.selected_images_listbox.delete(0, tk.END)

        # Add the selected images to the listbox
        for image_file_path in self.image_file_paths:
            # Get the file name from the file path
            _, file_name = os.path.split(image_file_path)
            self.selected_images_listbox.insert(tk.END, file_name)

    # Method to convert the images to PDF
    def convert_images_to_pdf(self):
        # Check if any images are selected
        if not self.image_file_paths:
            return

        # Get the output PDF file name
        output_pdf_file_path = (
            self.output_pdf_file_name.get() + ".pdf"
            if self.output_pdf_file_name.get()
            else "output.pdf"
        )

        # Create a PDF canvas
        pdf = canvas.Canvas(output_pdf_file_path, pagesize=(612, 792))

        # Iterate through the selected images
        for image_file_path in self.image_file_paths:
            # Open the image
            image = Image.open(image_file_path)

            # Calculate the available width and height for the image
            available_width = 540
            available_height = 720
            scale_factor = min(
                available_width / image.width, available_height / image.height
            )
            new_width = image.width * scale_factor
            new_height = image.height * scale_factor
            x_centered = (612 - new_width) / 2
            y_centered = (792 - new_height) / 2

            # Draw the image on the PDF canvas
            pdf.drawImage(
                image_file_path,
                x_centered,
                y_centered,
                width=new_width,
                height=new_height,
            )
            pdf.showPage()

        # Save the PDF
        pdf.save()


# Call the main function to start the application
main()

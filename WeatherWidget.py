import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import io

# OpenWeatherMap API key
API_KEY = "4dda36d4b10ecebc9313c967805937b9"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Function to fetch weather data
def get_weather(city="Riga"):  # Default location is Riga
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if data.get("cod") != 200:
            messagebox.showerror("Error", f"City not found: {city}")
            return None
        
        weather = {
            "city": data["name"],
            "temp": data["main"]["temp"],
            "desc": data["weather"][0]["description"].capitalize(),
            "icon": data["weather"][0]["icon"]
        }
        return weather

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"API request failed: {e}")
        return None

# Function to update weather details
def update_weather(event=None):
    city = city_entry.get().strip() if city_entry.get().strip() else "Riga"
    weather = get_weather(city)
    if weather:
        city_label.config(text=f"{weather['city']}")
        temp_label.config(text=f"{weather['temp']}°C")
        update_icon(weather['icon'])

# Function to update weather icon
def update_icon(icon_code):
    icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
    response = requests.get(icon_url)
    
    if response.status_code == 200:
        img_data = io.BytesIO(response.content)
        img = Image.open(img_data)
        img = img.resize((60, 60), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img)
        icon_label.config(image=img)
        icon_label.image = img

# Function to show search bar ONLY when hovering over city name
def show_search(event=None):
    search_frame.place(relx=0.5, rely=0.01, anchor="n")

# Function to hide search bar when not hovering over city name
def hide_search(event=None):
    search_frame.place_forget()

# Function to confirm and close the widget
def close_widget(event=None):
    confirm = messagebox.askyesno("Exit Widget", "Are you sure you want to close the weather widget?")
    if confirm:
        root.destroy()

# Creating the GUI window
root = tk.Tk()
root.title("Weather Widget")
root.geometry("180x110")
root.configure(bg="#444")
root.after(1500000, update_weather)
root.overrideredirect(True)

# Make the window draggable
def start_move(event):
    root.x = event.x
    root.y = event.y

def stop_move(event):
    root.x = None
    root.y = None

def do_move(event):
    x = root.winfo_x() + (event.x - root.x)
    y = root.winfo_y() + (event.y - root.y)
    root.geometry(f"+{x}+{y}")

root.bind("<ButtonPress-1>", start_move)
root.bind("<ButtonRelease-1>", stop_move)
root.bind("<B1-Motion>", do_move)

# Frame for search bar
search_frame = tk.Frame(root, bg="white", bd=2)
search_frame.place_forget()

# Entry field for city name
city_entry = tk.Entry(search_frame, font=("Arial", 12), bd=0, fg="black", bg="white", width=15)
city_entry.pack(side="left", padx=5, pady=5)

# Load search icon
search_img = Image.open("icons8-search-50.png").resize((18, 18), Image.Resampling.LANCZOS)
search_img = ImageTk.PhotoImage(search_img)

# Search button
search_button = tk.Button(search_frame, image=search_img, borderwidth=0, bg="white", command=update_weather)
search_button.pack(side="right", padx=2)

# Load refresh icon
refresh_img = Image.open("Refresh.png").resize((18, 18), Image.Resampling.LANCZOS)
refresh_img = ImageTk.PhotoImage(refresh_img)

# Refresh button - Placed at the bottom of the main window
refresh_button = tk.Button(root, image=refresh_img, borderwidth=0, bg="#444", command=update_weather)
refresh_button.pack(side="bottom", pady=2)  # Place it at the bottom
refresh_button.image = refresh_img  # Keep a reference

# Labels for displaying weather info
city_label = tk.Label(root, text="Riga", font=("Arial", 14, "bold"), bg="#444", fg="white")
city_label.pack(pady=5)

# Create a frame for icon and temperature
icon_temp_frame = tk.Frame(root, bg="#444")
icon_temp_frame.pack(pady=2)

# Weather Icon
icon_label = tk.Label(icon_temp_frame, bg="#444")
icon_label.pack(side="left", padx=2)

# Temperature Label
temp_label = tk.Label(icon_temp_frame, text="", font=("Arial", 20), bg="#444", fg="white")
temp_label.pack(side="left", padx=2)

# Bind hover event to city label
city_label.bind("<Enter>", show_search)
search_frame.bind("<Leave>", hide_search)

# Bind right-click event to close the widget
root.bind("<Button-3>", close_widget)

# Load default weather for Riga
update_weather()

# Run the GUI
root.mainloop()

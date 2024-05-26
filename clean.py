import os

def delete_csv_files(directory="."):
    try:
        for filename in os.listdir(directory):
            if filename.endswith(".csv"):
                os.remove(os.path.join(directory, filename))
                print(f"Deleted {filename}")
        print("All CSV files deleted successfully.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    delete_csv_files()

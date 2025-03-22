import csv
import http.client
import json

#Read the existing csv file
input_csv = 'kasarani sample 1.csv'
output_csv = 'kasarani ethnic.csv'

#Open the CSV file and read its contents
with open(input_csv, mode='r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    rows = list(reader) #convert to a list of dictionaries

    # Debugging: Print the headers and rows
    # print("Headers:", reader.fieldnames)
    # print("Rows:", rows)

#fetch data from API for each row

#Iterate through each row and call the API
for row in rows:
    # Debugging: Print the current row
    print("Current Row:", row)

    surname = row['SECONDARY_NAME']
    
    payload = json.dumps({
        "model": "deepseek-v3",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant that identifies Kenyan tribes based on surnames. You will receive a surname and you need to reply with a tribe. Just the one word tribe name"
            },
            {
                "role": "user",
                "content": surname  # Use the surname from the CSV
            }
        ]
    })

    #setup the API Connection
    conn = http.client.HTTPSConnection("deepseek-v31.p.rapidapi.com")
    headers = {
        'x-rapidapi-key': "17fe5cc679msh69819118f27cc82p13b3a2jsn913ce8d3f1cc",  # Replace with your RapidAPI key
        'x-rapidapi-host': "deepseek-v31.p.rapidapi.com",
        'Content-Type': "application/json"
    }

     # Make the API request
    conn.request("POST", "/", payload, headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")

    # Parse the API response
    try:
        api_response = json.loads(data)
        # Extract the tribe name from the API response
        tribe_name = api_response['choices'][0]['message']['content']
        row['TRIBE'] = tribe_name  # Add the tribe name to the new column
    except (KeyError, json.JSONDecodeError) as e:
        print(f"Error processing API response for surname: {surname}. Error: {e}")
        row['TRIBE'] = "Unknown"  # Default value if the API call fails

    # Close the connection
    conn.close()

    # Step 3: Write the updated data back to the CSV file
fieldnames = reader.fieldnames + ['TRIBE']  # Add the new column to the fieldnames
with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()  # Write the header
    writer.writerows(rows)  # Write the updated rows

print(f"Updated CSV saved to {output_csv}")



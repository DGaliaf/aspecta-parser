def deParseUserData(directory: str, filePath: str):
    user_data = {}
    with open(directory + filePath, 'r') as file:
        lines = file.readlines()

    current_section = None

    for line in lines:
        line = line.strip()

        if line.startswith("User:"):
            current_section = "User"
            user_data['User'] = {}
        elif line.startswith("-Name:"):
            user_data['User']['Name'] = line.split(": ", 1)[1].strip()
        elif line.startswith("-Wallet:"):
            user_data['User']['Wallet'] = line.split(": ", 1)[1].strip()

            with open("../output/wallets.txt", "a") as f:
                f.write(line.split(": ", 1)[1].strip() + "\n")
        elif line.startswith("-Labels:"):
            current_section = "Labels"
            user_data['User']['Labels'] = []
        elif line.startswith("-Label:") and current_section == "Labels":
            label = line.split(": ", 1)[1].strip()
            user_data['User']['Labels'].append(label)
        elif line.startswith("-Links:"):
            current_section = "Links"
            user_data['User']['Links'] = []
        elif line.startswith("-Link:") and current_section == "Links":
            link = line.split(": ", 1)[1].strip()
            user_data['User']['Links'].append(link)

    return user_data


if __name__ == "__main__":
    parsed_data = deParseUserData("../output/", "eligible.txt")
    print(parsed_data)

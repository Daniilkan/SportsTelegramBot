import json

def read_json(file):
    with open(file, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data
def write_json(file, data):
    with open(file, "w", encoding="utf-8") as file:
        file.write(json.dumps(data, indent=4, ensure_ascii=False))

def write_user(file, userID):
    data = read_json(file)
    if str(userID) in data:
        return
    else:
        data.update({str(userID) : {
            "Trains" : {

            }
        }})
        write_json(file, data)

def write_train(file, userID, day):
    data = read_json(file)
    data.update({userID : {
        "day" : day
    }})
    write_json(file, data)

def process_time(file, userID, time):
    data = read_json(file)
    data[str(userID)]["time"] = time
    write_json(file, data)

def add_write_time(file_4_schedule, userID, day,time):
    data = day
    data_4_train = read_json(file_4_schedule)
    if data in data_4_train[str(userID)]["Trains"]:
        newtime = data_4_train[str(userID)]["Trains"][data]
        newtime.append(time)
        data_4_train[str(userID)]["Trains"].update({data : newtime})
        write_json(file_4_schedule, data_4_train)
    else:
        user_trains = data_4_train[str(userID)]["Trains"]
        user_trains.update({data : [time]})
        data_4_train[str(userID)]["Trains"].update(user_trains)
        write_json(file_4_schedule, data_4_train)
def return_trains(file, userID):
    data = read_json(file)[str(userID)]["Trains"]
    final_message = "🗓Ваши текущие занятия: \n📌"
    for i in data:
        final_message += (i + ": ")
        for j in data[i]:
            final_message += (j + ", ")
        final_message += "\n📌"
    final_message = final_message[0:-4]
    return final_message
def delete_train(file, userID, time, day):
    data = read_json(file)
    newtimes = data[str(userID)]["Trains"][day]
    newtimes.remove(time)
    data[str(userID)]["Trains"][day] = newtimes
    if len(data[str(userID)]["Trains"][day]) == 0:
        data[str(userID)]["Trains"].pop(day)
    write_json(file, data)
def get_days(file, userID):
    data = read_json(file)
    return data[str(userID)]["Trains"]
def get_times(file, userID, day):
    data = read_json(file)
    return data[str(userID)]["Trains"][day]
def del_process(file, userID):
    data = read_json(file)
    del data[str(userID)]
    write_json(file, data)
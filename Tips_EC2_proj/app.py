from flask import Flask, request, render_template
import pickle

tips_app = Flask(__name__)
with open('Saved Model/tips_trained_model.pkl', 'rb') as file:
    trained_model = pickle.load(file)

sex_dict = {"Male": 1, "Female": 0}
smoker_dict = {"Yes": 1, "No": 0}
day_dict = {'Fri': 0, 'Thur': 1, 'Sat': 2, 'Sun': 3}
time_dict = {"Dinner": 1, "Lunch": 0}


@tips_app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@tips_app.route('/predict', methods=['POST'])
def prediction():
    total_bill = float(request.form['total_bill'])
    sex = [sex_dict[key] for key in sex_dict if key == request.form['sex']][0]
    smoker = [smoker_dict[key] for key in smoker_dict if key == request.form['smoker']][0]
    day = [day_dict[key] for key in day_dict if key == request.form['day']][0]
    time = [time_dict[key] for key in time_dict if key == request.form['time']][0]
    size = int(request.form['size'])

    pred = trained_model.predict([[total_bill, sex, smoker, day, time, size]])
    result = round(pred[0], 2)
    result_text = "On " + (request.form['day'] + "s" if request.form['day'] == 'Thur' else (
        request.form['day'] + "ur" if request.form['day'] == 'Sat' else request.form['day'])) + \
                  "day, " + ("a Non-smoker " if not smoker else "a Smoker ") + request.form[
                      'sex'] + " person of group size " + \
                  request.form['size'] + " with total bill of " + request.form[
                      'total_bill'] + " rupees will give a tip of " + \
                  str(result) + " rupees at " + request.form['time'] + " time."

    return render_template('index.html', pred_res=result_text)


if __name__ == '__main__':
    tips_app.run()  # Comment it when working with EC2
    # tips_app.run(host='0.0.0.0', port=8080) # Use this line when deploying it into EC2

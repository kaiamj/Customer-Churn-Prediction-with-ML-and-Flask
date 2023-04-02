from flask import Flask,request,render_template

from src.pipeline.predict_pipeline import CustomData,PredictPipeline

application=Flask(__name__)

app=application

## Route for a home page

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/predictdata',methods=['GET','POST'])
def predict_datapoint():
    if request.method=='GET':
        return render_template('home.html')
    else:
        data=CustomData(
            Age=int(request.form.get('Age')),
            FrequentFlyer=request.form.get('FrequentFlyer'),
            AnnualIncomeClass=request.form.get('AnnualIncomeClass'),
            ServicesOpted=int(request.form.get('ServicesOpted')),
            AccountSyncedToSocialMedia=request.form.get('AccountSyncedToSocialMedia'),
            BookedHotelOrNot=request.form.get('BookedHotelOrNot')         

        )
        pred_df=data.get_data_as_data_frame() # convert input values into dataframe
        print(pred_df)
        print("Before Prediction")

        predict_pipeline=PredictPipeline()
        print("Mid Prediction")
        results=predict_pipeline.predict(pred_df)
        print("after Prediction")
        return render_template('home.html',results=results[0])
    

if __name__=="__main__":
    app.run(host="0.0.0.0",debug=True)        


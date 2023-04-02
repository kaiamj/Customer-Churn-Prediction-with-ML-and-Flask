# transform data 

import sys
from dataclasses import dataclass

import numpy as np 
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler

from src.exception import CustomException
from src.logger import logging
import os

from src.utils import save_object

@dataclass
class DataTransformationConfig:
    # path of preprocessed file
    preprocessed_file_path = os.path.join('artifacts',"preprocessed.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()
    
    def make_pipeline(self):

        try:
            numerical_columns = ['Age', 'ServicesOpted']
            categorical_columns =  ['FrequentFlyer', 'AnnualIncomeClass', 'AccountSyncedToSocialMedia', 'BookedHotelOrNot']

            num_pipeline= Pipeline(
                steps=[
                ("imputer",SimpleImputer(strategy="median")),
                ("scaler",StandardScaler())

                ]
            )

            cat_pipeline=Pipeline(

                steps=[
                ("imputer",SimpleImputer(strategy="most_frequent")),
                ("one_hot_encoder",OneHotEncoder())
                ]

            )
            logging.info(f"Categorical columns: {categorical_columns}")
            logging.info(f"Numerical columns: {numerical_columns}")

            preprocessor=ColumnTransformer(
                [
                ("num_pipeline",num_pipeline,numerical_columns),
                ("cat_pipelines",cat_pipeline,categorical_columns)

                ]


            )

            return preprocessor
        
        except Exception as e:
            raise CustomException(e,sys)
        

    def initiate_tranformation(self,train_path,test_path):
        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            logging.info("Read train and test data completed")
            logging.info("Obtaining preprocessing object")

            preprocessing_obj=self.make_pipeline()  # preprocessor pipeline ready to transform df columns numerical, categorical
            
            target_column_name = 'Target'
            train_X=train_df.drop(columns=[target_column_name],axis=1)
            train_y=train_df[target_column_name]

            test_X=test_df.drop(columns=[target_column_name],axis=1)
            test_y=test_df[target_column_name]

            logging.info(
                f"preprocessing dataframes."
            )

            train_X_arr=preprocessing_obj.fit_transform(train_X)
            test_X_arr=preprocessing_obj.transform(test_X)

            train_arr = np.c_[ # concatenate vertically X = [[1,2],[3,4]] y = [1,0] - concatenate - [1,2,1],[3,4,0]
                train_X_arr, np.array(train_y)
            ]
            test_arr = np.c_[test_X_arr, np.array(test_y)]

            logging.info(f"Saving preprocessed obj")

            save_object(

                file_path=self.data_transformation_config.preprocessed_file_path,
                obj=preprocessing_obj

            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessed_file_path,
            )
        except Exception as e:
            raise CustomException(e,sys)
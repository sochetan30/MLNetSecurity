import sys
import os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networksecurity.constants.training_pipeline import TARGET_COLUMN
from networksecurity.constants.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS

from networksecurity.entity.artifact_entity import (
    DataTransformationArtifact,
    DataValidationArtifact,DataIngestionArtifact   
)

from networksecurity.entity.config_entity import DataTransformationConfig,DataValidationConfig
from networksecurity.exception.exception import NetworkSecurityException 
from networksecurity.logging.logger import logging
from networksecurity.utils.main_utils.utils import save_numpy_array_data,save_object


class DataTransformation:
    def __init__(self,data_validation_artifact: DataValidationArtifact,
                 data_validation_config: DataValidationConfig):

        try:
            self.data_validation_artifacts: DataValidationArtifact = data_validation_artifact
            self.data_transformation_config: DataTransformationConfig = data_validation_config

        except Exception as e:
            raise NetworkSecurityException(e, sys)


    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            df=pd.read_csv(file_path)
            return df
        except Exception as e:
            raise NetworkSecurityException(e, sys)


    def get_data_transformer_object(cls)-> Pipeline:

        logging.info("Entered get_data_transformer_object: method of transformationc class")


        try:
            imputer: KNNImputer =KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info(f"KNN imputer with {DATA_TRANSFORMATION_IMPUTER_PARAMS}")


            processor: Pipeline = Pipeline([("imputer", imputer)])
            return processor
        except Exception as e:
            raise NetworkSecurityException(e, sys)



    def intiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            logging.info("Entered intiate_data_transformation method in Data Transformation calss ")
            print('self.data_validation_artifacts.valid_train_file_path: ', self.data_validation_artifacts)
            train_df = DataTransformation.read_data(self.data_validation_artifacts.valid_train_file_path)
            test_df=DataTransformation.read_data(self.data_validation_artifacts.valid_test_file_path)

            #Implement kNN imputer
            # training Dataframe:
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_train_df= train_df[TARGET_COLUMN]
            target_feature_train_df= target_feature_train_df.replace(-1, 0)

            #Test Dataframe:
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df= test_df[TARGET_COLUMN]
            target_feature_test_df= target_feature_test_df.replace(-1, 0)
            logging.info("Starting Data transformation")

            preprocessor =self.get_data_transformer_object()
            preprocessor_object = preprocessor.fit(input_feature_train_df)
            transformed_input_train_feature = preprocessor_object.transform(input_feature_train_df)
            transformed_input_test_feature = preprocessor_object.transform(input_feature_test_df)

            train_arr = np.c_[transformed_input_train_feature, np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_input_test_feature, np.array(target_feature_test_df)]


            # SAve numpy array:
            print('self.data_transformation_config.transformed_train_file_path',self.data_transformation_config.transformed_train_file_path)
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, array=train_arr,)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, array=train_arr,)
            save_object(self.data_transformation_config.transformed_object_file_path, preprocessor_object,)

            # Saving artifacts 
            data_transformation_artifacts = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
                )
            return data_transformation_artifacts

        except Exception as e:
           raise NetworkSecurityException(e, sys)
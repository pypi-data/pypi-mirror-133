from pandas.core.frame import DataFrame
import streamlit as st
import seaborn as sns
import json,os
from kolibri.backend import models
from abc import ABC,abstractmethod


class KolibriImplements(ABC):
    """
    This is a abstract method for report implementation.
    """
    @abstractmethod
    def data(self):
        return NotImplementedError

    @abstractmethod
    def visualise(self):
        return NotImplementedError

    @abstractmethod
    def modelAnalysis(self):
        return NotImplementedError
    
    @abstractmethod
    def featureInteraction(self):
        return NotImplementedError


class Report(KolibriImplements):
    """
    A class which creates us the dashboard for our model and plots all the score and graph. This requires
    dataset as important parameter.
    """
    def __init__(self,data=None,model_interpreter=None,model_directory=None,X_test=None, X_train=None, y_test=None, y_train=None, x_val=None, y_val=None):
        """A constructor which takes the data, model_interpreter and the trainer as important parameter and 

        Args:
            data (Dataframe, optional): Pandas Dataframe(Dataset). Defaults to None.
            model_interpreter (ModelLoader, optional) : A model loader where we fetch all the training and test data Defaults to None.
            model_directory (String, optional): Directory path to fetch metetajson file. Defaults to None.
            X_test (List, optional): Defaults to None.
            X_train (List, optional): Defaults to None.
            y_test (List, optional): Defaults to None.
            y_train (List, optional): Defaults to None.
            x_val (List, optional): Defaults to None.
            y_val (List, optional): Defaults to None.
        """
        self.dataset = data
        self.model_directory = model_directory
        self.model_interpreter = model_interpreter
        self.X_test, self.X_train, self.y_test, self.y_train,self.x_val,self.y_val = X_test, X_train, y_test, y_train,x_val,y_val

    @st.cache(persist=True,suppress_st_warning=True)
    def convertTrainTestData(self) -> DataFrame:
        import pandas as pd
        # self.X_test, self.X_train, self.y_test, self.y_train = X_test, X_train, y_test, y_train

        # If the user provides list values then we convert it to dataframe

        X_test = pd.DataFrame(self.X_test)
        X_train = pd.DataFrame(self.X_train)
        y_test = pd.DataFrame(self.y_test)
        y_train = pd.DataFrame(self.y_train)
        x_val = pd.DataFrame(self.x_val)
        y_val = pd.DataFrame(self.y_val)
        return X_train,X_test,y_train,y_test,x_val,y_val

################################################### Overview Tab Starts ##########################################################
    @st.cache(persist=True,suppress_st_warning=True)
    def getInformation(self) -> tuple:
        """Reads the metajson file and fetches all the information required for the Overview tab.
        Returns:
            tuple: Returns kolibri version,date,time at which it executed and name of the model(s) used.
        """
        from datetime import datetime
        for i in os.listdir(self.model_directory):
            if i.endswith('.json'):
                fileOpen = self.model_directory+'/'+i
                f = open(fileOpen,'r')
                data = json.load(f)
                v = data['pipeline'][-1]['tunable']['model']['parameters']['estimators']['value']
                model_name = [i['class'].split('.')[-1] for i in v]
                kolibri_version = data['kolibri_version']
                trained_at,time_trained = data['trained_at'].split('-')
                time_finished = ":".join([time_trained[i:i+2] for i in range(0, len(time_trained), 2)])
                date = datetime.strptime(trained_at,'%Y%m%d').strftime('%d/%m/%Y')
        return (kolibri_version,date,time_finished,model_name)
    
    @st.cache(persist=True,suppress_st_warning=True)
    def data(self):
        '''
        This method displays description of the model, Model Version​,Kolibri Version​,Owner​ and Trained at​.
        '''
        kolibri_version,date,time_finished,model_name = self.getInformation()
        md = models.get_classification_model(model_name)
        st.subheader(f'Kolibri Version used is {kolibri_version}')
        st.subheader(f'Date completed {date} at {time_finished}')
        st.subheader(f'User: {os.environ.get("USER")}')
        st.subheader("Description of the model used")
        for i in range(len(md["parameters"]["estimators"]["value"])):
            name = md["parameters"]["estimators"]["value"][i]["name"]
            desc = md["parameters"]["estimators"]["value"][i]["description"]
            st.write(f"Name is {name}\nDescription used {desc}")
        st.table(self.dataset[:5])
################################################### Overview Tab Ends ############################################################
    
################################################### Class distribution Taxonmloy Starts ##########################################################
    @st.cache(persist=True,suppress_st_warning=True)
    def showVisualisation(self):
        X_train,X_test,y_train,y_test,x_val,y_val = self.convertTrainTestData()
        st.title('Visualising our dataset!!')
        if len(self.dataset.select_dtypes(include=["float", 'int']).columns) > 2:
                st.write(''' #### Heatmap for our dataset''')
                sns.heatmap(self.dataset.corr(),cmap='Greens')
                st.pyplot()
                with st.expander("See explanation"):
                    st.write("""The chart above shows some numbers class present in our dataset.""")
        else:
            import pandas as pd
            for i in os.listdir(self.model_directory):
                if i.endswith('.json'):
                    fileOpen = self.model_directory+'/'+i
                    f = open(fileOpen,'r')
                    data = json.load(f)
                    target = data['pipeline'][-1]['fixed']['target']
            # if we choose the options we get our output result as list
            col1,col2,col3 = st.columns([3,3,3])
            with col1:
                st.write(''' #### Train set Class distribution''')
                ax = pd.DataFrame(y_train.value_counts()).T.squeeze().plot(kind='bar')
                for p in ax.patches:
                    width = p.get_width()
                    height = p.get_height()
                    x, y = p.get_xy() 
                    ax.annotate(f'{height}', (round(x + width/2,2), round(y + height*1.01,2)), ha='center')
                    ax.set_xticklabels(y_test[0].unique())
                    ax.xaxis.set_label_text('Class')
                st.pyplot()
                with st.expander("See explanation"):
                    st.write("""The chart above shows some numbers class present in our dataset.""")
            
            with col2:
                st.write(''' #### Test set Class distribution''')
                ax = pd.DataFrame(y_test.value_counts()).T.squeeze().plot(kind='bar')
                for p in ax.patches:
                    width = p.get_width()
                    height = p.get_height()
                    x, y = p.get_xy() 
                    ax.annotate(f'{height}', (round(x + width/2,2), round(y + height*1.01,2)), ha='center')
                    ax.set_xticklabels(y_test[0].unique())
                    ax.xaxis.set_label_text('Class')
                st.pyplot()
                with st.expander("See explanation"):
                    st.write("""The chart above shows some numbers class present in our dataset.""")
            
            with col3:
                st.write(''' #### Validation set Class distribution''')
                ax = pd.DataFrame(y_val.value_counts()).T.squeeze().plot(kind='bar')
                for p in ax.patches:
                    width = p.get_width()
                    height = p.get_height()
                    x, y = p.get_xy() 
                    ax.annotate(f'{height}', (round(x + width/2,2), round(y + height*1.01,2)), ha='center')
                    ax.set_xticklabels(y_test[0].unique())
                    ax.xaxis.set_label_text('Class')
                st.pyplot()
                with st.expander("See explanation"):
                    st.write("""The chart above shows some numbers class present in our dataset.""")

    @st.cache(persist=True,suppress_st_warning=True)
    def visualise(self):
        self.showVisualisation()
################################################### Class distribution Taxonmloy Ends ############################################################    
    
################################################### Model Analysis Tab Starts ##########################################################    
    @st.cache(persist=True,suppress_st_warning=True)
    def fetchScores(self) -> tuple:
        """A method which fetch all the scores from the metajson file and plots all the result.
        Returns:
            tuple[Unbound | DataFrame, Unbound | DataFrame, Unbound | DataFrame, Unbound | Series]: Returns cf_matrix and all scores
        """
        import json,os,pandas as pd
        for i in os.listdir(self.model_directory):
            if i.endswith('.json'):
                fileOpen = self.model_directory+'/'+i
                f = open(fileOpen,'r')
                data = json.load(f)
                dict_val = [i for i in data['pipeline'] if 'performace_scores' in i][0]
                confussionMatrix = pd.DataFrame(dict_val['performace_scores']['confusion_matrix'])
                class_report = pd.DataFrame(dict_val['performace_scores']['class_report'])
                class_report.drop(class_report.index[len(class_report)-1],inplace=True) # Droping support
                new_class_report = class_report.iloc[: ,0:len(self.dataset[data['pipeline'][0]['fixed']['target']].unique())]
                score_report = class_report.iloc[:, 2:]
                res_score = dict([(k,dict_val['performace_scores'][k]) for k in dict_val['performace_scores'].keys() if k not in ['confusion_matrix', 'class_report']])
                res_score = pd.Series(res_score)
        return confussionMatrix,new_class_report,score_report,res_score

    
    @st.cache(persist=True,suppress_st_warning=True)           
    def modelAnalysis(self):
        """This is a function where it plots all the score analysis such as precision,recall,f1-score and 
        accuracy.
        """
        import numpy as np
        confussionMatrix,class_report,score_report,res_score = self.fetchScores()
        col1,col2= st.columns(2)
        with col1:
            st.write(''' #### Confusion Matix for our dataset''')
            sns.heatmap(confussionMatrix/np.sum(confussionMatrix), annot=True, fmt='.2%')
            st.pyplot()
            with st.expander("See explanation"):
                st.write("""A random text about confusion matrix""")
        
        with col2:
            st.write(''' #### Class Report for our dataset''')
            ax1 = class_report.plot(kind='bar',figsize=(6,6))
            for p in ax1.patches:
                width = p.get_width()
                height = p.get_height()
                x, y = p.get_xy() 
                ax1.annotate(f'{height:.0%}', (round(x + width/2,2), round(y + height*1.02,2)), ha='center')
            st.pyplot()
            with st.expander("See explanation"):
                st.write("""A random text about confusion matrix""")
        # st.write(score_report,'\n',res_score)

        col3,col4= st.columns(2)
        with col3:
            st.write(''' #### Accuracy,Macro Average and Weighted Average for our dataset''')
            ax1 = res_score.plot(kind='bar', color=['black', 'red', 'green', 'blue', 'coral','limegreen','darkkhaki','thistle','chocolate','peru','darkgoldenrod','steelblue'])
            for p in ax1.patches:
                width1 = p.get_width()
                height1 = p.get_height()
                x1, y1 = p.get_xy() 
                ax1.annotate(f'{height1:.0%}', (round(x1 + width1/2,2), round(y1 + height1*1.02,2)), ha='center')
            st.pyplot()
            with st.expander("See explanation"):
                st.write("""A random text about confusion matrix""")
################################################### Model Analysis Tab Ends ############################################################    
    
    @st.cache(persist=True,suppress_st_warning=True)
    def featureInteraction(self):
        """Checking our feature how it interacts with other feature. We provde you a dropbox 
        functionality and then you can analyse the interactn fo the features.
        """
        pass

    # @st.cache(persist=True,suppress_st_warning=True)
    def run(self):
        st.page_config = st.set_page_config(
                page_title="Kolibri report",
                layout="wide",
            )
        st.set_option('deprecation.showPyplotGlobalUse', False)

        self.data() # Ovireview tab
        self.visualise() # Extra Info {yet to think about this tab}
        self.modelAnalysis() # Model analysis tab
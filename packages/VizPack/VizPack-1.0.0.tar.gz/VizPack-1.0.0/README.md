# **VizPack**
> **VizPack** is a Visualization package with necessary tools for plotting visualizations from Pandas DataFrame  

<br/><br/>
### **Data Visualization**
- To install the VizPack project, run this command in your terminal:
```python 3
$ pip install VizPack
```
- Import the Visualization Class from the vizpack module, for visualizing pandas DataFrame
``` python 
>>> from VizPack.vizpack import Viz_Func
```
- Initialize a variable to work with the Viz_Func object
```python
>>> viz = Viz_Func()

========== Welcome to the Visualization Tool kit ========== 

```
- Checking for Documentation
```python
>>> help(viz)
```

- **Examples of Valid use**
> **Extensively Analysed** [here](https://github.com/invest41/VizPack/blob/main/Package%20Analysis/Viz_Package.ipynb)
1.
```python
# Labelling the plot 
>>> viz.label_plot(
                    title ='Distribution plot of Greek Alphabet', 
                    x = 'Count',
                    y ='Alphabet')

# Plotting the Bars
>>> plots = viz.plot_bar(
                         dataset = df, 
                         limit = 10, 
                         column ='C', 
                         horizontal = True, 
                         figsize = (16,8), 
                         color = 'maroon')

#Anotating the Bars 
>>> viz.annot_bar(plots, horizontal = True)
```
![GreekPlot](https://github.com/invest41/VizPack/blob/main/Package%20Analysis/GreekPlot.png)
<br/><br/>

2.
```python
viz.plot_donut(dataset = df,
               limit = 7, 
               column = 'C', 
               title = 'Plot: Distribution of Greek Alphabets',
               shadow = False,
               explode = False, background = 'white'
               )
```
![GreekDonut](https://github.com/invest41/VizPack/blob/main/Package%20Analysis/GreekDonut.png)

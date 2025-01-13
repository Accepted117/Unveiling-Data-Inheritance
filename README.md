# Unveiling-Data-Inheritance
Insights from Artificial Intelligence Applications in Pesticide Development

The drug.csv and Pesticide.csv are the original datasets.\n
The molecular complexity calculation refers to the method of Adrian et al. Details can be found in https://github.com/frog2000/Spacial-Score.\n
The /Molecular_Retrosynthesis/ folder records the results of molecular complexity calculations. \n
The inverse synthesis analyses refer to the methodology of Samuel et al. A detailed description is available at http://www.github.com/MolecularAI/aizynthfnder.\n
The /Retrosynthesis/ 1.reaction_route_predict/ directory, documenting the results of the first predicted synthetic route (where drug.csv was renamed Chembl_drug.csv). \n
The results are pooled within /result_data/, the reaction_route.csv file records the aggregated results of the reaction route predictions. The drug and pest directories, record the datasets of the drug as well as the pesticide cuts, and output.json records the results of the reaction route predictions.
The molecular generation references the method of Hannes H. et al, a detailed description of which is available at https://github.com/MolecularAI/REINVENT4
The /price_predict/2.gen_mol/ directory records the result records of the generated models.
The assessment of the drug-like properties of newly generated drugs is informed by the methodology of G. Richard et al. The pesticide-like properties of the newly generated pesticides were assessed with reference to the method of Yang et al.
The /New_Molecules/ folder for newly generated drug/pesticide molecules and their property predictions respectively.
The /TSNE/ folder records chemical distribution of drug/pesticide molecules.

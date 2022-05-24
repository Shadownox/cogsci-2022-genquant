cogsci-2022-genquant
====================

Companion repository for the 2022 article "Generalizing Syllogistic Reasoning: Extending Syllogisms to General Quantifiers" published in the proceedings of the 44rd Annual Meeting of the Cognitive Science Society.

# Overview

- `analysis`: Contains the analysis scripts generating the results and figures from the paper.
- `analysis/comparison.py`: Script for comparing the Ragni2016 dataset (traditional syllogisms) to the Ragni2021 dataset (generalized quantifiers). Generates a plot visualizing both patterns (*Figure 1*) and calculates the RMSE.
- `analysis/correct_conclusions.py`: Helper file containing a dictionary with the logically correct responses for all 144 syllogisms with the quantifiers *All*, *Some*, *Some not*, *No*, *Most* and *Most not*.
- `analysis/correctness.py`: Plots the correctness by syllogism type (*Figure 3* and *Figure 4*).
- `analysis/genquant_corr_traditional_corr`: Plots the correctness of participants on traditional and generalized syllogisms (*Figure 6*).
- `analysis/misinterpreted`: Plots the correctness when accounting for misinterpreted meanings of the quantifiers (*Figure 5*).
- `analysis/pattern_collapsed.py`: Plots the response behavior with focus on the quantifiers (*Figure 2*).
- `data`: Contains the datasets
- `data/Ragni2016.csv`: Ragni2016 dataset from the CCOBRA framework containing responses to traditional syllogisms.
- `data/Ragni2021.csv`: Responses to all 144 syllogisms with the quantifiers *All*, *Some*, *Some not*, *No*, *Most* and *Most not*.

# Analysis Scripts

### Dependencies

- Python 3
    - CCOBRA
    - pandas
    - numpy
	- matplotlib
    - seaborn
    - scipy

### Usage

After downloading the repository, navigate to the analysis subfolder:

```
cd /path/to/repository/analysis
```

All scripts can be executed without entering additional parameters. The scripts will create the plots in the same folder. To execute the scripts, enter: 

```
$> python [script].py
```

### References

Brand, D., Mittenbühler, M., & Ragni, M. (2022). Generalizing Syllogistic Reasoning: Extending Syllogisms to General Quantifiers. In proceedings of the 44rd Annual Meeting of the Cognitive Science Society.

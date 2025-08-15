# PSDF: A Multi-Level Feature-Based Ponzi Scheme Detection Framework for Smart Contracts in Ethereum

Hongliang Zhang School of Computer Science and Technology, Qilu University of Technology, Jinan, 250353, China*

Jie Zhang

School of Computer Science and Technology, Qilu University of Technology, Jinan, 250353, China†

Zihao Wu

School of Computer Science and Technology, Qilu University of Technology, Jinan, 250353, China†

Received (Day Month Year) Revised (Day Month Year)

The Ethereum ecosystem is currently confronted with significant challenges due to the emergence of Ponzi schemes in smart contracts, which weakens trust in decentralized finance and exposes unsuspecting investors to potential risks. To tackle the issue, this paper proposes a Ponzi scheme detection framework (PSDF) based on multi- level features, which is the framework specifically designed to detect Ponzi scheme smart contracts for eliminating model bias. Specifically, PSDF extracts bytecode features and combines them with account features to obtain initial features without relying on the source code of smart contracts. Subsequently, the Ponzi network model (PonziNet) is designed in the framework to detect smart contract Ponzi schemes, which consists of a CNN- based feature extractor and a decision classifier using LightGBM. Experimental results show that PSDF can accurately detect the smart contract Ponzi schemes in Ethereum, which improves the trust of users in the platform. Our code is publicly available at https://github.com/Federatedzhang/PSDF.

Keywords: Ethereum ecosystem; Machine learning; Smart contract; Ponzi scheme; Feature extractor; Decision classifier.

# 1. Introduction

Ethereum, a decentralized blockchain platform with smart contract capability, has experienced rapid development in the cryptocurrency field. Currently, it is ranked second in terms of market capitalization and occupies a crucial position in the realm of digital assets 1,2. Therefore, Ethereum is widely used in supply chain finance 3, commerce 4, cryptocurrencies 5, securities 6, and insurance 7.

While Ethereum is growing rapidly, it faces the security challenge of lacking robust auditing solutions for smart contracts. The challenge has led to fraudulent activities, such as Ponzi schemes deployed on Ethereum, which has caused serious property losses to investors  $^{8}$ . Ponzi schemes (e.g., Charles Ponzi) are fraudulent schemes in which fraudsters use funds from new investors to pay off previous investors, rather than through legitimate transactions or actual investment returns  $^{9}$ . Thus, the investors are both beneficiaries and victims. Nowadays, Ponzi schemes on Ethereum have caused huge financial losses. Therefore, it is urgent to design effective methods for detecting and reviewing smart contracts on Ethereum  $^{10}$ .

At present, many solutions are proposed to detect Ponzi scheme smart contracts, such as rule- based, graph analysis- based, and machine learning- based methods. Concretely, Rule- based solutions rely on predefined rules or heuristics to identify Ponzi schemes  $^{11,12,13}$ . However, the solutions have difficulty adapting to the dynamic nature of Ponzi schemes and identifying the complex variables in the smart contracts  $^{14}$ . Graph analysis- based solutions focus on analyzing relationships within smart contracts to identify potential Ponzi schemes and anomalous behavior  $^{15,16,17}$ . Yet, the solutions struggle to construct comprehensive and representative graphs that accurately capture the characteristics of Ponzi schemes, especially in large- scale smart contracts  $^{18}$ . Meanwhile, both above solutions rely on the source code of smart contracts, which leads to the fact that auditing tools based on the above solutions fail to detect non- open- sourced smart contracts, which limits their detection scope  $^{19}$ . Machine learning- based solutions utilize large datasets to train models that can detect Ponzi schemes  $^{20}$ . Nevertheless, machine learning- based solutions make it difficult to extract key features of Ponzi schemes, which makes it difficult to accurately identify Ponzi contracts  $^{21}$ . Meanwhile, only a few smart contracts are identified as Ponzi contracts on Ethereum, leading to model bias in these schemes because their models are trained based on class- imbalanced training data, which causes the models that are skewed for the majority class  $^{22,23,24}$ .

To overcome these limitations, a Ponzi scheme detection framework (PSDF) is proposed based on multi- level features to detect Ponzi scheme smart contracts. Specifically, PSDF combines bytecode features, account transaction features, multi- level feature engineering, and a PonziNet model to realize detection. First, the PSDF uses the smart contract's bytecode and account information to obtain the initial features of the smart contract. Second, PSDF adopts the SMOTE- Tomek algorithm and multi- level feature engineering to convert initial features into multi- level features, where the multi- level features capture the fine- grained level properties and coarse- grained level characteristics of smart contracts and implement the class- balance of training data. Finally, the PSDF utilizes PonziNet for the task of identifying smart contract Ponzi schemes, which includes a CNN- based feature extractor and a decision classifier with LightGBM. Concretely, the feature extractor extracts optimal features from multi- level features, and then the optimal features are input into the decision classifier to get detection results. Through these unique combinations, the PSDF significantly improves the accuracy of Ponzi scheme detection. The main contributions can be summarized as follows.

- A Ponzi Scheme Detection Framework is proposed for Smart Contracts in Ethereum, which can extract bytecode features and combine them with account features to identify Ponzi schemes without relying on the source code of smart contracts, and expand the deployment of PSDF.- PSDF can eliminate model bias by achieving class-balanced training data to detect Ponzi scheme smart contracts.- PSDF can construct multi-level features from extracted both bytecode features and account features for data enhancement, which captures the fine-grained level properties and coarse-grained level characteristics smart contracts.- A PonziNet model is designed in PSDF for the task of identifying smart contract Ponzi schemes. Meanwhile, extensive experiments demonstrate the superiority of PSDF compared to existing schemes.

The rest of the paper is structured as follows. Section II provides an overview of current solutions for detecting Ponzi scheme smart contracts. Section III introduces the opcodes of Ethereum and Ponzi scheme. Section IV presents the proposed PSDF framework. Section V discusses experimental results, and Section VI concludes the research in the paper.

# 2. Related Work

In this section, existing works are discussed on detecting Ponzi scheme smart contracts, and the feasibility of PSDF is analyzed.

# 2.1. Ponzi Scheme Detection on Blockchain

Blockchain technology has sparked a global investment boom, but its technical complexity makes it more difficult for investors to identify the Ponzi schemes hidden in smart contracts. According to Cryptoanalysis, a virtual currency investigation and risk analysis company, Ponzi- related frauds on Ethereum amount to $725 million 25. To detect fraudulent activities on the blockchain, machine learning algorithms have been employed to develop an effective detection scheme 26,27. In 28, Chen et al. utilized the XGBoost algorithm to automatically detect Ponzi scheme smart contracts. However, the algorithm fails to solve the issue of class- imbalanced training data, which leads to model bias. Toyoda et al. proposed a method for identifying high- yield accounts based on the frequency of bitcoin transactions, which provides guidance for detecting potential Ponzi scheme smart contracts 29. But the method relies on the frequency of Bitcoin transactions and ignores other more representative and comprehensive characteristics of smart contracts. Ibba et al. trained machine learning models that utilized both account features and bytecode features of smart contracts as input features. The effectiveness of the features is evaluated by Decision Trees (DT), Support Vector Machines (SVM), and Naive Bayes (NB) algorithms 30. Chen et al. proposed a SADPonzi detection method based on symbolic execution. The method detects Ponzi schemes by analyzing the contract bytecode, extracting semantic information, and identifying investor- related trading behaviors 16. However, the SADPonzi is limited to bytecode review and does not involve transaction history. Jin et al. designed a module for

enhancing features of smart contracts, which captures information from account behavior and employs machine learning techniques to detect Ponzi scheme smart contracts  $^{31}$ , but when the transaction scale of smart contracts is relatively large, it is difficult to capture information about account behavior. He et al. extracted sequence features and account features from smart contracts, which the authors then fed into a random forest algorithm to detect Ponzi schemes  $^{32}$ . However, random forests have limitations for dealing with highly complex, non- linear, or highly correlated data.

Due to the significant advantages that deep learning has shown in various fields, researchers are gradually applying it to detect Ponzi scheme smart contracts. Concretely, Hu et al. proposed SCSGuard, a deep learning fraud detection framework  $^{33}$ . The framework designs an attention neural network to analyze code features for detecting Ponzi scheme smart contracts. Due to the complexity and diversity of the code, the functionality and behavior of smart contracts cannot just be represented by code features. In  $^{34}$ , Luo et al. converted contract bytecodes to grayscale images. Due to the different lengths of bytecodes, they designed a spatial pooling algorithm to improve the CNN's ability to better handle grayscale images with inconsistent sizes. Although the detection method is novel, it ignores the problem of model bias due to class- imbalanced training data. Wang et al. introduced the SMOTE algorithm to solve class- imbalanced training data for Ponzi detection, which eliminated the model bias  $^{35}$ . Although the problem is solved, the algorithm tends to cause the appearance of duplicate data, which negatively affects the model's accuracy and generalization capability.

# 2.2. Feasibility Analysis of the PSDF

Our research is developed on the basis of previous work, as inspired by some of the following. Note that in  $^{32}$ ,  $^{35}$ , and  $^{36}$ , the authors highlighted the problem of class- imbalanced training data. To solve this problem, PSDF integrates the SMOTE- Tomek algorithm to implement class- balanced training data, which can significantly eliminate model bias. Furthermore, multi- level feature engineering is inspired by  $^{37}$ . Although the application scenarios are different, the work inspires our thinking. By considering both fine- grained level properties and coarse- grained level characteristics of smart contracts, PSDF captures a comprehensive understanding of smart contract behavior. In addition, Zhang et al. used the LightGBM algorithm to detect Ponzi contracts and obtain good results  $^{38}$ . Thus, the algorithm is incorporated into our PonziNet model.

By highlighting the connection to related work, PSDF not only includes previous technologies but also designs new components such as PonziNet, which allows PSDF to overcome the limitations of existing methods and provide a more accurate detection mechanism for Ponzi scheme smart contracts.

# 3. Preliminaries

The section introduces some important preliminaries, including bytecode, opcode, and Ponzi contracts.

# 3.1. Bytecode and Opcode

Solidity is the most popular high- level language for writing smart contracts 39. When creating a smart contract written in Solidity, the source code cannot be executed directly on the Ethereum Virtual Machine (EVM). Ethereum needs to compile the source code of a smart contract into bytecode and then store it as bytecode on Ethereum. Concretely, the preparation phase consists of three processes: installing the compilation tool, writing the contract in Solidity, and starting the Ether node. Then, the compiler compiles the smart contract source code into bytecode. Finally, the miner uploads the verified bytecode to Ethereum.

EVM can store up to 256 different types of bytecodes, each with a different function. There is a one- to- one correspondence between opcodes and bytecodes, and each opcode corresponds to a bytecode. The appendix of the Ethereum Yellow Paper contains a complete list of bytecodes and their corresponding opcodes 40.

# 3.2. Ponzi Contract

Algorithm 1, known as the Crystal Doubler, is a critical part of the execution of the Ponzi contract, which can be found at etherscan.io. The meaning of variables in the algorithm is described in Table 1.

Table 1: Variable meaning in the Ponzi contract.  

<table><tr><td>Variable</td><td>Meaning</td></tr><tr><td>Total Player</td><td>Total number of depositors.</td></tr><tr><td>Balance</td><td>Current balance of the contract.</td></tr><tr><td>Total Deposited</td><td>Total number of deposits.</td></tr><tr><td>Total Paid_Out</td><td>Total payment of smart contract.</td></tr><tr><td>Amount</td><td>Amount of funds deposited by a depositor.</td></tr><tr><td>Depositors</td><td>List of depositors.</td></tr><tr><td>Payout</td><td>Amount of payments to depositors.</td></tr><tr><td>nr</td><td>Index of a depositor.</td></tr></table>

When a Ponzi contract is deployed on Ethereum, it initializes several variables. The depositor (investor) can enter the contract by providing a deposit amount. The contract keeps track of the depositor through the list of depositors and updates Total- Player, Balance, and Total Deposit. Then, the contract starts the payment process by iterating the list of depositors and assigning payments to the previous depositors. The payout operation is executed when the balance of the contract is sufficient to cover  $200\%$  of the original amount invested by the previous depositor. Finally, the contract adjusts the Balance and Total_Paid_Out variables accordingly.

The flow of funds for the Ponzi contract is shown in Figure 1. Only early depositors in Ponzi contracts will receive a return. If no subsequent funds are invested in Ponzi contracts,

  
Fig. 1: The flow of funds in a Ponzi contract.

the capital chain will be broken, and later depositors will lose money. When the amount of investment in the Ponzi contract reaches a certain threshold, the cryptocurrency will experience a thunderstorm that eventually affects the normal functioning of the Ethereum- driven industry.



  
Fig. 2: Overall framework of the PSDF.

# 4. The Design of PSDF

This section provides a comprehensive introduction to the PSDF framework, including the overall process, initial feature construction, data balancing, multi- level feature engineering, and the development of the PonziNet model.

# 4.1. Overall Process

This subsection summarizes the overall process of the PSDF framework, as shown in Figure 2. Specifically, the transaction information and compiled bytecodes are obtained from the Ethereum website<sup>a</sup> based on the addresses of smart contracts in the dataset. Subsequently, the compiled bytecodes are transformed into opcodes using a disassembler, so the opcode features of each smart contract are constructed by calculating the frequency of opcode calls. Meanwhile, transaction features are extracted from the transaction information as the account features of a smart contract. Thus, the initial features of each smart contract consist of both code features and account features.

To address the class- imbalanced training data, PSDF adopts the SMOTE- Tomek algorithm to deal with the problem, which effectively solves the class- imbalanced training data in detecting Ponzi scheme smart contracts. Next, multi- level feature engineering includes both fine- grained level and coarse- grained level construction to convert initial features into multi- level features of smart contracts. Finally, the PonziNet model consists of two main components: a feature extractor and a LightGBM classifier. The feature extractor is used to

extract optimal features from multi- level features, and then the optimal features are input to the decision classifier for detecting Ponzi scheme smart contracts. Specifically, this paper constructs a multi- level characterization of smart contracts. In order to better capture the Ponzi logic in the multi- level features, we need to extract the optimal features from the multi- level features with a feature extractor. After extracting the optimal features, we need to detect the optimal features to get the final classification result, thus, a decision classifier is needed to detect the Ponzi contract.

# 4.2. Initial Feature Construction

Given a smart contract dataset  $\mathcal{D}$ , which comes from previous studies 41. The ratio of positive to negative samples is approximately 12:1. The dataset contains addresses and labels for smart contracts. In the initial feature construction, a total of 9 opcode features and 7 account features are extracted as the initial data of smart contracts based on the dataset  $\mathcal{D}$ . Next, the construction process for these features is described in detail.

Table 2: Function of the Opcodes.  

<table><tr><td>Opcode</td><td>Function</td></tr><tr><td>GT</td><td>Block gas limit of the current block.</td></tr><tr><td>EP</td><td>Exponential operation.</td></tr><tr><td>CD</td><td>Loading data from the input.</td></tr><tr><td>SD</td><td>Loading a value from address-specific memory.</td></tr><tr><td>CR</td><td>Returning the address of the account.</td></tr><tr><td>LT</td><td>Bitwise operator.</td></tr><tr><td>GS</td><td>Returning the current amount of gas.</td></tr><tr><td>MD</td><td>Modulus operation.</td></tr><tr><td>ME</td><td>Storing a value at the specified address.</td></tr></table>

# 4.2.1. Opcode Features

The frequency of calls of opcodes is analyzed in smart contracts according to the previous study. Wang et al. obtained a ranking of their effectiveness in detecting Ponzi scheme smart contracts 35. Among these opcodes, the 9 most influential opcodes in order for Ponzi scheme detection are GASLIMIT (GT), EXP (EP), CALLDATALOAD (CD), SLOAD (SD), CALLER (CR), LT, GAS (GS), MOD (MD), and MSTORE (ME), where  $(\cdot)$  denotes the short form of the opcode. The specific functions of the opcodes are shown in TABLE 2. Based on the above opcodes, the frequency calls of these 9 opcodes are used as opcode features of our scheme. In other words, PSDF utilizes the above 9 opcode features to conduct Ponzi scheme detection.

  
Fig. 3: The distribution proportion of opcode features between normal contracts and Ponzi contracts.

Meanwhile, the proportion of 9 opcode features between normal contracts and Ponzi contracts is calculated, as shown in Figure 3. The distribution of opcodes shows that the EP and ME opcodes are more common in the normal contract, while the LT, SD and CR opcodes are more common in the Ponzi contract, which indicates a difference in the frequency of opcode calls between the two classes. This is mainly due to the fact that Ponzi contracts frequently call comparison operators (i.e., LT) and load data from memory (i.e., SD) when there is a new inflow of funds in order to implement the ponzi process. Conversely, a normal contract does not have a fixed number of opcodes to be executed when funds flow into the contract due to the absence of Ponzi logic, which results in the difference in a proportion of opcodes between normal contracts and Ponzi contracts. Meanwhile, unsupervised cluster analysis is performed for the 9 opcode features in the smart contract dataset. Figure 4 shows a clear boundary of the 9 opcode features between normal contracts and Ponzi contracts, which proves that there are significant differences between them. Therefore, the 9 opcode features can be used to detect Ponzi contracts.

  
Fig. 4: A Scatter plot of opcode features between normal contracts and Ponzi contracts.

# 4.2.2.Account Features

Compared to normal contracts, Ponzi contracts have significant differences in account trading characteristics, especially in terms of currency circulation during contract trading. Through manual review, we can generalize the differences in account characteristics between normal contracts and Ponzi contracts. In Ponzi contracts, only a limited number of early contract investors can earn significant returns, and most of the returns are concentrated among the early investors. In particular, the creator of Ponzi contract received the highest rewards. Meanwhile, Ponzi contracts tend to maintain modest balances while distributing investment returns quickly. Therefore, 7 distinct features are obtained from account transactions as account features to identify Ponzi contracts.

Num_inv: This feature represents the number of investments in each contract. Assuming that each contract consists of  $n$  trades and that each trade is initiated by a transaction account address, the calculation formula of Num_inv can be expressed as follows:

$$
\mathrm{Num\_inv} = \sum_{i = 1}^{n}a_{i},1\leq i\leq n. \tag{1}
$$

where the number of trade per investment is denoted as 1, so we have  $a_{i} = 1$

Num- pay: This feature represents the number of payment trades in each contract. If there are  $l$  payment trades per contract, and each trade involves an expense to a specific account address, the calculation of Num- pay can be expressed as follows:

$$
\mathrm{Num\_pay} = \sum_{j = 1}^{l}b_{i},\quad 1\leq j\leq l, \tag{2}
$$

where the number of trade per payment is denoted as 1, and we have  $b_{i} = 1$

Max- pay: The maximum number of expenses from one contract account to another is defined as Max- pay. Assuming that there are  $c$  expenses in each contract, where  $d$  expenses into account  $S$  then the formula is as follows:

$$
\mathrm{Max\_pay} = \left\{ \begin{array}{ll}d, & \mathrm{if}~d\geq \mathrm{max},\\ \mathrm{max}, & \mathrm{if}~d< \mathrm{max},\\ 0, & \mathrm{if}~c = 0, \end{array} \right. \tag{3}
$$

where max is the maximum number of expenses pointing to the same account  $S$  in addition to  $d$

Paid_rate: This feature represents the percentage of investors who have received at least one payment. It can be calculated as the percentage of the number of investors who received a payment  $(N_{\mathrm{received}})$  to the total number of investors involved  $(N_{\mathrm{total}})$  , so it can be expressed as:

$$
\mathrm{P a i d\_r a t e} = \frac{N_{\mathrm{r e c e i v e d}}}{N_{\mathrm{t o t a l}}}. \tag{4}
$$

- Bal: This feature represents the balance of smart contract, indicating the amount of funds held within the contract at a given time point. It reflects the total value of assets stored in the contract and can be treated as the remaining or available funds after deducting any trades.- D_ind: This feature represents the difference between the investment and payment amounts of all investors in the smart contract. Assuming there are  $p$  investors in the contract and  $V$  is a vector of length  $p$ , where  $M_i$  and  $N_i$  denote the investment and payment amounts of the  $i$ -th investor, respectively. To calculate the difference between investments and payments, each element of the vector  $V$  is computed as  $V[i] = N_i - M_i$ . Then D_ind is obtained by the following formula:

$$
\mathrm{D_{-}ind} = \left\{ \begin{array}{ll}0, & p< 3\\ s, & p\geq 3 \end{array} \right., \tag{5}
$$

where  $p \geq 3$  is a limit to ensure that there are a sufficient number of investors in the contract before calculating the difference D_ind. The variable  $s$  represents the skewness of the set  $\{V_{[1]}, V_{[2]}, \ldots , V_{[p]}\}$ , which is calculated by formula (6). For Ponzi contracts, the value of D_ind is usually negative, indicating that the majority of investors have minimal rewards.

$$
s = \frac{\sqrt{p(p - 1)}}{p - 2}\left[\frac{\frac{1}{p}\sum_{i = 1}^{p}\left(V[i] - \bar{V}\right)^3}{\left(\frac{1}{p}\sum_{i = 1}^{p}\left(V[i] - \bar{V}\right)^2\right)^{\frac{3}{2}}}\right] \tag{6}
$$

- Kr: This feature represents the percentage of investors who invest before receiving the reward. A high Kr indicates that the contract primarily attracts investors who are already aware of the investment opportunity. In the case of the Ponzi scheme, a very high Kr is expected to be observed, as these schemes tend to attract informed investors who are willing to invest before receiving any reward.

To verify the effectiveness of the above account features, account features from the dataset are extracted for statistical analysis. Figure 5 shows significant differences between Ponzi contracts and normal contracts in the mean of the 7 account features. This is due to the account features of Ponzi contracts that are different from normal contracts, because as long as there is a new inflow of funds into Ponzi contracts, the funds flow regularly according to the settings of Ponzi contracts, highlighting the statistical differences between Ponzi contracts and normal contracts. Specifically, the mean value of Num_Inv is clearly higher for normal contracts compared to Ponzi contracts. This is because the number of investments in Ponzi schemes can only increase with the addition of new investors, while the number of investments in normal contracts increases because of normal trading. In addition, there are differences in the contract balance (Bal) between Ponzi contracts and normal contracts. This is because normal contracts can store funds normally, whereas Ponzi contracts transfer funds to other accounts as soon as they reach a threshold that triggers a financing trade. The other features also show differences in their statistical distributions.

Notably, the mean values of Paid_rate, D_ind, and Kr are close to 0, but they are still slightly different. Therefore, these seven statistical differences in accounts reflect the differences between Ponzi scheme contracts and normal contracts and provide a basis for Ponzi scheme detection.

  
Fig. 5: The differences of account features between normal contracts and Ponzi contracts.

# 4.3. Data Balance

Following the above initial feature construction steps, both account and opcode features about smart contracts are obtained in dataset  $\mathcal{D}$  to form dataset  $\mathcal{Q}$ . Specifically,  $\mathcal{Q}$  is represented as  $\{(X_i,y_i)\}_{i = 1}^M$ , where  $M$  denotes the number of smart contracts in the dataset,  $X_{i}$  is the feature vector that concatenates the account and opcode features of the  $i$ - th contract, and  $y_{i}$  is the corresponding class label. If  $y_{i} = 1$ , the  $i$ - th contract denotes a normal contract, while  $y_{i} = 0$  denotes that the  $i$ - th contract is a Ponzi contract. Let's compose the normal contracts into the dataset  $\mathcal{Q}_n$ , and the Ponzi into  $\mathcal{Q}_f$ , so  $\mathcal{Q} = \mathcal{Q}_n\cup \mathcal{Q}_f$  is obtained. In  $\mathcal{Q}_n$  and  $\mathcal{Q}_f$ , there is a significant difference in the number of contracts in these two classes, i.e.,  $|\mathcal{Q}_n|\gg |\mathcal{Q}_f|$ . Therefore, the  $\mathcal{Q}$  dataset belongs to the class imbalance.

To address the class imbalance under dataset  $\mathcal{Q}$ , the SMOTE- Tomek is used to solve the issue. Specifically, SMOTE- Tomek combines SMOTE (Synthetic Minority Over- sampling Technique) and Tomek- Link. On the one hand, the mechanism of SMOTE is to generate new minority class samples by inserting between the feature vectors of two neighboring minority classes to enhance minority class. On the other hand, the mechanism of Tomek- Link seeks out pairs of instances from different classes that are very close to each other, and removes these pairs. The following describes the detailed process of SMOTE- Tomek.

# 4.3.1. SMOTE

SMOTE is an oversampling algorithm that balances the dataset by generating synthetic samples for a minority class. Zhang et al. used the algorithm to balance the smart contract dataset to detect Ponzi contracts in their scheme, which effectively improves the detection

38. In the SMOTE-Tomek, the smote algorithm first needs to be executed. The steps of the SMOTE algorithm are described as follows:

Step 1: For a normal contract  $X_{i}$  of dataset  $\mathcal{Q}_j$  , SMOTE calculates the Euclidean distance between  $X_{i}$  and other samples of  $\mathcal{Q}_f$  to find the near- neighbor samples  $k$  of  $X_{i}$  Step 2: SMOTE randomly selects one sample from the near- neighbor samples  $k$  of  $X_{i}$  , denoted as  $X_{j}$  Step3: SMOTE generates a new sample  $X_{g}$  by randomly selecting a point between the feature vectors of  $X_{j}$  and  $X_{j}$  using the formula:

$$
X_{g} = X_{i} + \mathrm{rand}(0,1)*|X_{i} - X_{j}|. \tag{7}
$$

# 4.3.2.Tomek-Links

In SMOTE- Tomek, the Tomek- Links algorithm needs to be executed after SMOTE. The Tomek- Links algorithm is used to reduce the overlapping samples between different classes in the dataset 42. Specifically, it selects a pair of samples, the one  $(X_{f})$  from the  $\mathcal{Q}_f$  and the other one  $(X_{n})$  from the  $\mathcal{Q}_n$  , and calculates their distance  $O(X_{f},X_{n})$  . If there exists a sample  $X_{i}$  in the dataset  $\mathcal{Q}$  , regardless of its class, that satisfies  $O(X_{f},X_{i})< O(X_{f},X_{n})$  or  $O(X_{n},X_{i})< O(X_{f},X_{n})$  , this indicates that  $X_{f}$  and  $X_{n}$  do not overlap. However, if a sample  $X_{i}$  does not exist,  $X_{f}$  and  $X_{n}$  form a Tomek pair, indicating that the samples overlap. Finally, samples of this Tomek pair are removed from the dataset  $\mathcal{Q}$

After applying the SMOTE- Tomek algorithm to address the class imbalance, the dataset  $\mathcal{Q}_1$  is obtained, which means that the  $\mathcal{Q}_1$  is class- balanced. To further improve the feature representation of smart contracts, multi- level feature engineering is performed on the  $\mathcal{Q}_1$  dataset.

# 4.4. Multi-level Feature Engineering

Multi- level feature engineering is the process of capturing multi- level features from the feature vector  $X_{i}$ . The multi- level features are divided into fine- grained features and coarse- grained features. The fine- grained features provide detailed properties of a smart contract, while the coarse- grained features reflect the characteristics of a smart contract. Here, "property" refers to specific and detailed attributes of a smart contract, whereas "characteristic" pertains to overall traits that define a smart contract's nature.

To conveniently describe the multi- level engineering process,  $\mathcal{Q}_1$  is denoted as:

$$
\mathcal{Q}_1 = \{(X_1,y_1),(X_2,y_2),\ldots ,(X_n,y_n)\} ,
$$

where  $X_{i} = (A_{i},B_{i})$  denotes the feature vector of smart contract,  $A_{i}$  denotes the account features,  $B_{i}$  denotes the opcode features, and  $y_{i}$  denotes the label of  $i$ - th smart contract. Thus, the set of account features is denoted as  $\mathcal{A} = \{A_1,A_2,\ldots ,A_n\}$ , the set of opcode features is denoted as  $\mathcal{B} = \{B_1,B_2,\ldots ,B_n\}$ , and the set of feature vectors is denoted as  $\mathcal{X} = \{X_1,X_2,\ldots ,X_n\}$ .

# 4.4.1. Fine-grained Features Construction

In the set  $\mathcal{X}$  , three specific features, namely Num_inv, Num_Pay, and D_ind, have significantly larger value ranges compared to the other account features. When using  $\mathcal{X}$  for Ponzi scheme detection, differences in feature magnitude can mask the importance of other features, which affect the performance of the model. To address this issue, the  $\mathbb{Z}$  score (standard score) normalization method is adopted to handle the features. By calculating the  $\mathbb{Z}$  score for each feature, the feature values are converted into normalized units based on their respective means and standard deviations. So  $F_{i} =$  normalization  $(X_{i})$  can be obtained, where  $F_{i} = (A_{i}^{\prime},B_{i}^{\prime})$  denotes the normalized feature vector, while  $A_{i}^{\prime}$  and  $B_{i}^{\prime}$  denote the normalized account features and opcode features, respectively. After the normalization process, the feature vector  $F_{i}$  consists of normalized account features and opcode features, which is defined as the fine- grained features. Meanwhile, the dataset  $\Omega_2$  from  $\Omega_1$  is obtained, where  $\mathcal{Q}_2 = \{(F_1,y_1),(F_2,y_2),\ldots ,(F_n,y_n)\}$

To verify the effectiveness of fine- grained features, a simple unsupervised learning clustering method is used based on dataset  $\Omega_2$  to view boundaries between normal contracts and Ponzi contracts. The feature boundary is shown in Figure 6. We can observe that the boundary between Ponzi contracts and normal contracts is very clear, which further implies that there is a large feature difference between the different classes. Therefore, fine- grained features are available to detect Ponzi contracts.

  
Fig. 6: The scatter plot of fine-grained features between normal contracts and Ponzi contracts.

# 4.4.2. Coarse-grained Features Construction

The initial features of the  $i$ - th smart contract consist of account features  $A_{i}$  and opcode features  $B_{i}$ , which represents two different perspectives. The smart contract is represented by considering the account features as a whole and the opcode features as another whole. To

this end, the account features are compressed as one integral feature and the opcode features as another integral feature. Here, the  $t$ - distribution stochastic nearest neighbor embedding ( $t$ - SNE) method is adopted to map the high- dimensional data to the low- dimensional space 43. Therefore, the  $d_{i} = t\text{- SNE} (A_{i})$  and  $h_{i} = t\text{- SNE} (B_{i})$  are used to construct the coarse- grained feature of smart contracts. Given  $G_{i} = (d_{i},h_{i})$  as coarse- grained features of  $i$ - th smart contract, where  $d_{i}$  represents the coarse- grained account feature (Coarse- A) of  $i$ - th smart contract and  $h_{i}$  represents the coarse- grained opcode feature (Coarse- O) of  $i$ - th smart contract.

The fine- grained features  $F_{i}$  and the coarse- grained features  $G_{i}$  are concatenated to form the multi- level features  $T_{i}$ ,

$$
\mathcal{Q}_3 = \{(T_1,y_1),(T_2,y_2),\ldots ,(T_n,y_n)\} ,
$$

where  $T_{i} = (F_{i},G_{i})$ , and  $T$  is finally input to the PonziNet model.

  
Fig. 7: Information gain analysis of multi-level features.

# 4.4.3. Analysis of Multi-level Features

Information gain is utilized to validate the effectiveness of multi- level features  $T$  for detecting Ponzi scheme smart contracts. Information gain is a commonly used feature selection method that measures the contribution of features to classification tasks 44. If the multilevel features have high information gain, it shows their important role in detecting Ponzi scheme smart contracts and verifies the rationality and effectiveness of multi- level features.

The result is shown in Figure 7, where coarse- grained features rank higher in terms of information gain, indicating that they are most capable of capturing the features of Ponzi contracts. In addition, SD and LT also rank higher in terms of information gain, indicating

that they contribute to detect Ponzi scheme smart contracts. The information gain analysis confirms the effectiveness of multi- level features in PSDF.

# 4.5. The Design of PonziNet

This paper designs a PonziNet model in PSDF, the model combines CNN and LightGBM algorithms with the architecture shown in Figure 8. Specifically, PonziNet uses CNN as a feature extractor to extract optimal features from multi- level features. LightGBM is then used as a classifier to output the final result. Therefore, PonziNet consists of a feature extractor and a decision classifier. It is worth noting that the feature extractor and the decision classification are two separately trained models. Therefore, the task of detecting Ponzi contracts is defined as a binary classification problem.

  
Fig. 8: PonziNet Model Architecture.

# 4.5.1. Feature Extractor

In the feature extractor, the optimal features are extracted from the multi- level features. Specifically, the feature vector  $T_{i} = (F_{i},G_{i})$  in dataset  $Q_{3}$  is divided into  $F_{i}$  and  $G_{i}$  which are padded separately in order to improve the subsequent convolution operation. So, the  $F_{i}^{\prime} = pad(F_{i})$  and  $G_{i}^{\prime} = pad(G_{i})$  are obtained, where  $pad()$  denotes padding operation.

After the padding step, the padded features  $F_{i}^{\prime}$  and  $G_{i}^{\prime}$ , are concatenated to form the matrix  $M_{i}$  to merge fine- grained and coarse- grained features. The  $M_{i}$  contains the multilevel features of the  $i$ th smart contract. Next, the  $M_{i}$  is input to CNN.

Since  $M_{i}$  is a single- channel feature map of dimension, each filter in CNN uses a convolution kernel of size  $k \times 1$  to perform a single- channel convolution. To extract key features,  $J$  filters of the same size are convolved with the matrix  $M_{i}$ . Formula (8) represents the convolutional feature extraction computation:



$$
C_{\mathrm{out}}[i] = f\left(\sum_{j = 0}^{j = (k - 1)}M[z + j]\times W[j] + b\right), \tag{8}
$$

where  $C_\mathrm{out}$  represents the output feature map obtained from the convolutional operation,  $\mathcal{Z}$  denotes the position in the output feature map  $(0\leq z\leq J)$  ,and  $j$  represents the index of the convolution kernel ranging from O to  $(k - 1)$  . The input feature  $M$  is convolved with learnable weights  $W$  , and the resulting feature map is passed through an activation function  $f(\cdot)$  . Additionally, a bias term  $b$  is added to the convolution. So  $Y = CNN(M)$  is obtained, where  $CNN(\cdot)$  denotes the whole convolution process, where  $Y$  can be interpreted as the high- level feature.

The Softmax layer performs a softmax operation on the output  $Y$  of the convolution layer, and converts the value to the probability of its corresponding class, where  $Y = (y_1', y_2', \dots , y_q')$ . The softmax formula is as follows:

$$
Y^{\prime} = \mathit{Sofmax}(Y) = \left(\frac{e^{y_1^{\prime}}}{\sum_{q = 1}^{R}e^{y_q^{\prime}}}\dots \frac{e^{y_q^{\prime}}}{\sum_{q = 1}^{R}e^{y_q^{\prime}}}\right) \tag{9}
$$

where  $Y'$  denotes the probability set that the sample corresponds to each class,  $R$  denotes the number of sample classes in the task, and  $\frac{e^{y_q'}}{\sum_{q = 1}^{R} e^{y_q'}}$  denotes probability when the sample belongs to the  $q$ - th class.

During the training process, our goal is to minimize the following objective function:

$$
Obj(\theta) = L_{e}(\theta) + \Omega (\theta), \tag{10}
$$

where  $L_{e}(\theta)$  is the loss function of the feature extractor, which is used to measure how well the model fits the training data, and  $\Omega (\theta)$  is the regulation, which is used to measure the complexity of the learned model. Minimizing the  $Obj(\theta)$  means minimizing the  $L_{e}(\theta)$  and  $\Omega (\theta)$  at the same time, which can get the model out of the state of underfitting and optimize the regulation term for avoiding overfitting the model.

The loss function plays a crucial role in the performance of the model, it should usually be chosen explicitly to apply. Here, considering that the model is a binary classification, the cross- entropy loss function is chosen. This is because the cross- entropy loss function effectively penalizes those misclassified samples and pushes the model to adjust in the right direction. The function is shown in formula (11), which  $l_{q}$  value is 1 when the sample belongs to  $q$ - th class, otherwise it is 0.

$$
L_{e}(\theta) = -\sum l_{q}\cdot \log \frac{e^{y_{q}^{\prime}}}{\sum_{q = 1}^{R}e^{y_{q}^{\prime}}} \tag{11}
$$

The most basic regularization method is to add a penalty to the original loss function, and the  $L_{2}$  norm is used as follows:

$$
\Omega (\theta) = \eta \| \pmb {m}\| ^2, \tag{12}
$$

where  $\eta$  is importance weight and

$$
\| \pmb {m}\| ^2\equiv \pmb {m}^T\pmb {m} = m_0^2 +m_1^2 +\ldots +m_K^2, \tag{13}
$$

which  $m_{K}$  denotes the  $K$ - th weight parameter of the model. After training the feature extractor, the model is saved.

After the feature extractor is trained, the trained model is used to extract the optimal features from the multi- level features in order to classify them in the decision classifier. Specifically, the dataset  $\mathcal{Q}_3$  is input into the feature extractor. At this point, the optimal features  $H$  of the previous layer of Softmax in the feature extractor are obtained, and the dataset  $\mathcal{Q}_4$  is obtained from  $\mathcal{Q}_3$ , where  $\mathcal{Q}_4 = \{(H_1,y_1),(H_2,y_2),\ldots ,(H_n,y_n)\}$  for training the decision classifier.

# 4.5.2. Decision Classifier

In the decision classifier, the  $\mathcal{Q}_4$  dataset needs to be categorized to get the final detection result. Specifically, the decision classifier uses a machine learning algorithm called LightGBM, which is described next. LightGBM is now extensively used in many different domains (e.g., classification, regression and ranking) 45. The LightGBM algorithm combines weak models into strong ones using an iterative process.

More specifically, given the dataset  $\mathcal{Q}_4$ , PSDF adopts the LightGBM algorithm to train decision classifier. The difference with the traditional techniques (e.g., XGBoost and GBDT) is that Light GBM adopts a vertical tree growth approach instead of the horizontal tree growth used by other algorithms. This unique characteristic enables LightGBM to efficiently handle large- scale data and features, making it an effective method of data processing.

After the decision classifier is trained, the parameters of the classifier are saved for evaluating our solution. Finally, Algorithm 2 summarizes the PonziNet model.

# 5. Experiments

The dataset 41 is used from the website, which contains 131 Ponzi contracts and 1513 normal contracts. It crawls data from Ethereum.io according to the contract address, so the dataset provides us with smart contract addresses and labels. The additional smart contract information needs to be obtained from the public website.

After the dataset is balanced with the SMOTE- Tomek algorithm,  $70\%$  of the dataset is extracted as the train set, and the remaining  $30\%$  is extracted as the test set. The experiments analyses of PSDF are performed below.

# 5.1. Experimental Environment

To conduct accurate and reproducible experiments, it is essential to provide a comprehensive description of the experimental environment. Table 3 shows the detailed configuration in our study. The Torch library is employed for constructing the feature extractor. Simultaneously, the LightGBM library is utilized to implement the decision classifier, obtaining the corresponding code from https://github.com/microsoft/LightGBM.

Table 3: Experiment Environment.  

<table><tr><td>Component</td><td>Configuration</td></tr><tr><td>CPU</td><td>Intel Core i7-8700K @ 3.70GHz</td></tr><tr><td>GPU</td><td>NVIDIA GeForce RTX 1060</td></tr><tr><td>Memory</td><td>16 GB DDR4 RAM</td></tr><tr><td>Storage</td><td>1 TB SSD</td></tr><tr><td>Operating System</td><td>Windows 10</td></tr><tr><td>Python</td><td>3.11.5</td></tr><tr><td>Torch</td><td>2.1.0+cu118</td></tr><tr><td>CUDA</td><td>12.2</td></tr></table>

# 5.2. Experimental Metrics

To accurately evaluate the performance of the model and to facilitate comparison with other Ponzi contract detection methods, we use metrics such as accuracy, precision, recall and F- score for evaluation. Specifically, Accuracy and Precision are the most commonly

used assessment measures for classification. The Recall is critical for many application scenarios, especially in demanding areas such as fraud detection. The F1- score is a metric that balances precision and recall. With the higher of the above indicators, it means that the performance of our scheme is better and the detection results are more accurate. On the contrary, it means the worse the detection results. The objective of our scheme is to make these four evaluation metrics as high as possible. The specific definitions are as follows.

$$
\mathrm{Accuracy} = \frac{\mathrm{true positive} + \mathrm{true negative}}{\mathrm{all}} \tag{14}
$$

$$
\mathrm{Precision} = \frac{\mathrm{true positive}}{\mathrm{true positive} + \mathrm{false positive}} \tag{15}
$$

$$
\mathrm{Recall} = \frac{\mathrm{true positive}}{\mathrm{true positive} + \mathrm{false negative}} \tag{16}
$$

$$
\mathrm{F1 - score} = 2\times \frac{\mathrm{precision}\times\mathrm{recall}}{\mathrm{precision} + \mathrm{recall}} \tag{17}
$$

# 5.3. Experimental Parameter Setting

In the PSDF, the input to the feature extractor of PonziNet are coarse- grained level features and fine- grained level features. Next, the output dimension of each layer and the number of trainable parameters are set in the feature extractor, as shown in Table. 4. Finally, the effect of hyper parameters (epoch, batch size and test set ratio) in the feature extractor on the experimental results is explored in the following experiments.

Table 4: Feature Extractor Structure and Number of Trainable Parameters.  

<table><tr><td>Layer (type:depth-idx)</td><td>Output Shape</td><td>Param #</td></tr><tr><td>Linear: 1 – 1</td><td>1 × 1 × 5</td><td>15</td></tr><tr><td>Linear: 1 – 2</td><td>1 × 1 × 20</td><td>340</td></tr><tr><td>Linear: 1 – 3</td><td>1 × 1 × 25</td><td>-</td></tr><tr><td>Conv1d: 2 – 1</td><td>- × 1 × 25</td><td>4</td></tr><tr><td>ReLU: 2 – 2</td><td>1 × 1 × 25</td><td>-</td></tr><tr><td>Conv1d: 2 – 3</td><td>1 × 1 × 25</td><td>4</td></tr><tr><td>ReLU: 2 – 4</td><td>1 × 1 × 25</td><td>-</td></tr><tr><td>Linear: 1 – 4</td><td>1 × 8</td><td>208</td></tr><tr><td>Linear: 1 – 5</td><td>1 × 2</td><td>18</td></tr></table>

# 5.3.1. The Impact of epochs for PSDF

We evaluate the performance of PSDF by adjusting the parameters of PonziNet. In PonziNet, an epoch represents one training for each sample in the train set. However, a single epoch of the dataset may not be sufficient for effective training. Therefore, multiple iterations are required to improve the performance of the model. In addition, as the epochs increase, the model state goes from underfitting to overfitting. Thus, choosing the appropriate number of epochs is crucial to obtain the best training results.

In our experiments, we set the learning rate to 0.001 and assigned  $20\%$  of the data to the test set with a fixed batch size of 20 and all settings unchanged except epoch. We start training from the 20- th epoch and increased the epoch value by 20 in each subsequent experiment. We conduct 11 experiments with different epochs, each experiment repeats 10 times. The average accuracy is calculated as the final result, as shown in Figure 9. The experimental results show that the accuracy of the test set gradually improves as the number of epochs increases. However, after reaching 60 epochs, the accuracy of the test set starts to drop. For the phenomenon of accuracy rising and then suddenly going down, this is because too few epochs can lead to an underfitting of the model to the highest effect. However, too much epoch can lead to overfitting of the model. As a result, the experimental results appear to rise and then go down.

  
Fig. 9: The impact of epoch on accuracy in PSDF.

To strike a balance between model performance and overfitting, we conclude that 60 epochs is the optimal value. This decision aims to achieve a satisfying level of accuracy while minimizing the negative performance of overfitting.

# 5.3.2. The Impact of Batch Size for PSDF

In our experiments, we analyze the effect of batch size on PSDF. Choosing an appropriate batch size is crucial because it affects both the model's convergence and computational

efficiency. This is because different batch sizes are one of the hyperparameters that affect both the performance of the model and the training rate, so we test the accuracy and training time of the model. To conduct our experiments, we keep a fixed test set ratio of  $20\%$ , set the number of training epochs to 60, and use a learning rate of 0.001. We vary the batch size from 1, 32, 64, 128, 256, to 512. Figure 10 shows the training time and test set accuracy for different batch sizes.

From the experimental results, we find that batch sizes larger than 64 decrease the accuracy of the PSDF. This is because larger batch sizes cause the scheme to converge more slowly and skip smaller local minima, which affects the accuracy of the scheme. Specifically, if the batch size is too small, the training time of the model is long, the training efficiency is low, and it also makes the model difficult to converge, which leads to underfitting. On the contrary, if the batch size is too large, it can reduce the training time, but it can cause the model generalization ability to decrease. When the batch size exceeds 32, the time required for training remains essentially the same. Therefore, we set the batch size to 64, which strikes a balance between training time and model accuracy.

  
Fig. 10: The impact of batch size on accuracy for PSDF.

# 5.3.3. The Impact of Test set Ratio for PSDF

In PonziNet models, the choice of test set ratio plays a crucial role in evaluating the performance of the scheme to generalize to unknown data. In this experiment, we analyze the effects of different test set ratios on the parameters of PSDF. We set the learning rate to 0.001, the batch size fixed to 64, and the epoch set to 60. We evaluate the performance of the model by setting different test set ratios (including  $10\%$ ,  $20\%$ ,  $30\%$ , and  $40\%$ ). The accuracy of PSDF is shown in Figure 11.

With an increasing ratio of testset, the accuracy of PSDF decreases. This decrease can be attributed to the reduced availability of training data, which limits the ability of the model to learn and capture the underlying patterns and complexity of the Ponzi contract. The phenomenon emphasizes the importance of having sufficient training data. Sufficient

training data allows the model to learn from a wide variety of Ponzi contract examples, thereby improving its understanding associated with such contracts. With a larger train set, the model can better generalize and make informed predictions about unknown data, improving its overall accuracy. Based on these findings, we set the test set ratio to  $30\%$ . This selection strikes a balance between ensuring an adequate train set and reserving enough data for testing. All in all, after extensive experimental exploration, we finally set the epoch to 60, the batch size to 64, and the test set ratio to  $30\%$ .

  
Fig. 11: The impact of test set ratio for PSDF.

# 5.4. Experiment Comparison

# 5.4.1. Comparison with Other Schemes

The experimental results highlight the effectiveness of different Ponzi scheme detection methods, and are evaluated by performance metrics such as accuracy, precision, recall, and F1- score. In fraud detection, the recall should be increased as possible while maintaining precision. The main reason is that the raw dataset is out of proportion between positive and negative. In addition, XGBoost, LightGBM, RF, SVM, LR, and KNN are baseline methods, which do not do anything with the data. We also compare with state- of- the art methods, such as SPP- CNN  $^{34}$ , PD- SECR  $^{36}$ , and SCSGuard  $^{33}$  and Scheme  $^{46}$ .

The comparison results are shown in Table 5. Specifically, we can observe that common machine learning methods (i.e., baseline methods) have high accuracy, but the other three metrics are very low. This is due to the fact that these baseline methods do not perform data balancing, leading to the phenomenon of model bias. The SPP- CNN  $^{34}$ , PD- SECR  $^{36}$ , SC- SGuard, and Scheme  $^{46}$  methods also show good performance in Ponzi contract detection. They effectively mitigate the class imbalance problem in detection by using data balancing techniques. Mitigating the effects of imbalanced class distributions can improve their detection capabilities. However, these schemes only use fine- grained opcode features as data for model training. In addition, PSDF shows superior performance in all evaluation metrics.

This is due to the fact that we construct the multi- level features of smart contracts that can be captured from both fine- grained and coarse- grained perspectives. The high F1- score in PSDF indicates its strong ability to accurately identify Ponzi schemes, making it a robust and reliable method for Ponzi scheme detection.

Table 5: Detection Performance among Different Scheme.  

<table><tr><td>Model</td><td>Data balance</td><td>Accuracy</td><td>Precision</td><td>Recall</td><td>F1-score</td></tr><tr><td>XGBoost</td><td>No</td><td>96.7</td><td>80.0</td><td>69.6</td><td>74.4</td></tr><tr><td>LightGBM</td><td>No</td><td>96.9</td><td>88.2</td><td>65.2</td><td>75.0</td></tr><tr><td>RF</td><td>No</td><td>97.3</td><td>88.9</td><td>69.6</td><td>78.0</td></tr><tr><td>SVM</td><td>No</td><td>93.6</td><td>99.3</td><td>18.6</td><td>16.0</td></tr><tr><td>LR</td><td>No</td><td>93.0</td><td>50.0</td><td>43.5</td><td>46.5</td></tr><tr><td>KNN</td><td>No</td><td>92.7</td><td>47.7</td><td>39.3</td><td>42.8</td></tr><tr><td>SPP-CNN 34</td><td>Yes</td><td>95.8</td><td>98.2</td><td>93.8</td><td>95.9</td></tr><tr><td>PD-SECR 36</td><td>Yes</td><td>97.9</td><td>96.7</td><td>99.3</td><td>98.1</td></tr><tr><td>SCSGuard 33</td><td>No</td><td>92.2</td><td>96.3</td><td>97.8</td><td>97.1</td></tr><tr><td>Scheme 46</td><td>Yes</td><td>96.0</td><td>92.3</td><td>94.1</td><td>95.8</td></tr><tr><td>PSDF</td><td>Yes</td><td>98.3</td><td>99.1</td><td>97.8</td><td>98.3</td></tr></table>

# 5.4.2. Effectiveness Analysis of Multi-level Feature

To evaluate the effectiveness of multi- level feature on Ponzi scheme detection, we set up two sets of experiments with the PSDF. In the first set of experiments, fine- grained features are used to input the PonziNet, and in the second set of experiments, multi- grained features are used to input the PonziNet. The results, as shown in Fig. 12, which clearly demonstrate the effectiveness of multi- level features. The second set of experiments achieves an accuracy rate  $0.8\%$  higher than the first set, highlighting the significant contribution of multi- level features in improving the performance of PSDF.

By merging features at different levels, PSDF allows for a more comprehensive understanding of the data, capturing the attributes and overall characteristics of smart contracts. Fine- grained level features provide a more granular analysis of smart contracts and better represent the potential characteristics of smart contracts associated with Ponzi schemes. Coarse- grained level features capture the characteristics of smart contracts as a whole, allowing the model to capture overall patterns in the data.

# 5.4.3. The Impact of SMOTE-Tomek Algorithm for PSDF.

In our scheme, we use the SMOTE- Tomek algorithm to balance the classes of the dataset for mitigating model bias. In order to evaluate the impact of SMOTE- Tomek on PSDF, we conducted experiments with four scenarios, namely, raw data, SMOTE, Tomek- links, and

  
Fig. 12: Effectiveness of different level feature in PSDF.

SMOTE- Tomek. Meanwhile, the results are presented in the form of confusion matrices, as shown in Figure 13a to Figure 13d.

Comparing the four confusion matrices, we observe that after applying the SMOTE- Tomek algorithm, the classification accuracy for the minority class samples is significantly improved and the model bias phenomenon is eliminated, which indicates that the algorithm effectively solves the class imbalance problem in the dataset. In the situation of raw data, the model bias phenomenon is very serious. Although it will have high accuracy, it fails for Ponzi contract detection.

The experimental results further validate the effectiveness of the SMOTE- Tomek algorithm in dealing with imbalanced datasets. The improved classification results show that the application of the SMOTE- Tomek algorithm successfully balances the dataset and improves the ability of the model to correctly classify minority classes.

# 6. Conclusion

In conclusion, PSDF is an effective method specifically designed to detect Ponzi schemes in smart contracts. According to detailed experimental results, PSDF shows excellent performance in identifying Ponzi contracts.

PSDF differs from other techniques used to detect various vulnerabilities in smart contracts, because it is specifically designed for Ponzi scheme detection. Ponzi schemes involve deceptive financial practices and fraudulent investment schemes, requiring a unique approach that focuses on capturing and analyzing financial patterns and user behavior within smart contracts. PSDF is specifically tailored to address these specific characteristics of Ponzi schemes, enabling accurate identification and detection of Ponzi scheme smart contracts.

PSDF has broader applications in the analysis and classification of smart contracts beyond Ponzi detection. It can assist auditors, regulators, and platform operators in monitoring and ensuring the integrity of smart contracts within blockchain ecosystems. PSDF can

  
Fig. 13: Confusion matrix for Ponzi contract detection with different sampling techniques.

conduct ponzi detection based on the features of smart contracts, which becomes an important tool for detecting and preventing fraudulent activities in the Ethereum- based derivative space.

In our future work, we have the following to improve. We need to continue to test or evaluate the generalization ability of our scheme with more or more complex data. In addition, in this paper, we focus only on Ponzi schemes in smart contracts. However, in real- world scenarios, there are other dangers or vulnerabilities in smart contracts, which can also cause huge losses in Ethereum. Therefore, we focus on other vulnerabilities of smart contracts, such as timestamp dependency, overflow of operations, etc., to ensure the security of Ethereum.

# References

1. L. Liu, W. Tsai, M. Bhuiyan, H. Peng and M. Liu, Blockchain-enabled fraud discovery through abnormal smart contract detection on ethereum, *Future Gener. Comput. Syst.* **128** (2022) 158-166.  
2. J. Wu, K. Lin, D. Lin, Z. Zheng, H. Huang and Z. Zheng, Financial crimes in web3-empowered metaverse: Taxonomy, countermeasures, and opportunities, *IEEE Open J. Comput. Soc.* **4** (2023) 37-49.
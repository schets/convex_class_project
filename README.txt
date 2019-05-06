Project organization:

data: The data downloading script, provided matrices, and the end destination for downloaded emails is here
python: Python code to run the models is here
report: The latex, images, and pdf are here
final: A copy of the final project is here

Running the code:

First, one needs to have python3.7 at least.
Second, will require the numpy, scipy, matplotlib, and cvxpy libraries. These can be installed on a linux or mac with
pip install numpy scipy matplotlib cvxpy
One may need to run pip3, or another versioned pip, if multiple pythons are installed.

The 4 runnable programs are:

  * stemmer.py: This will stem each word passed as input and print the results
  * process_email.py: This will process email in a file and print the output.
  * run_example.py: This runs the svm on randomly generated data to generate example plots
  * run_report.py: This runs the svm on downloaded emails and returns the scores

Each program can be passed the --help argument to get a description of the parameters, and can be run with python <program_name> arg1 arg2

For example:

Samuels-MacBook-Pro:python samuelschetterer$ python run_report.py --data ../data --train 0.2 --weight 0.1 --use-download

ECOS 2.0.7 - (C) embotech GmbH, Zurich Switzerland, 2012-15. Web: www.embotech.com/ECOS

It     pcost       dcost      gap   pres   dres    k/t    mu     step   sigma     IR    |   BT
 0  +1.309e-02  +1.219e+03  +4e+03  2e-01  8e+00  1e+00  2e+00    ---    ---    2  1  - |  -  -
 1  +1.113e+00  +2.176e+02  +1e+03  5e-02  1e+00  6e-01  5e-01  0.8050  1e-01   2  1  1 |  0  0
 2  +8.736e-01  +9.064e+01  +5e+02  2e-02  4e-01  2e-01  2e-01  0.8146  3e-01   2  2  2 |  0  0
 3  +8.775e-01  +2.241e+01  +1e+02  8e-03  1e-01  4e-02  5e-02  0.9013  2e-01   2  2  2 |  0  0
 4  +8.718e-01  +7.119e+00  +4e+01  3e-03  3e-02  1e-02  1e-02  0.7835  9e-02   3  3  3 |  0  0
 5  +7.248e-01  +2.814e+00  +1e+01  9e-04  8e-03  3e-03  5e-03  0.7940  1e-01   3  3  3 |  0  0
 6  +6.012e-01  +1.509e+00  +5e+00  4e-04  4e-03  1e-03  2e-03  0.7635  2e-01   3  3  3 |  0  0
 7  +5.463e-01  +1.168e+00  +3e+00  2e-04  3e-03  8e-04  1e-03  0.5673  4e-01   3  3  3 |  0  0
 8  +5.043e-01  +8.062e-01  +2e+00  1e-04  1e-03  3e-04  7e-04  0.7652  4e-01   3  3  3 |  0  0
 9  +4.898e-01  +7.004e-01  +1e+00  8e-05  9e-04  2e-04  4e-04  0.6318  5e-01   2  2  2 |  0  0
10  +4.688e-01  +5.373e-01  +4e-01  3e-05  3e-04  7e-05  2e-04  0.8498  2e-01   3  3  3 |  0  0
11  +4.587e-01  +4.812e-01  +1e-01  9e-06  9e-05  2e-05  5e-05  0.8071  2e-01   2  2  2 |  0  0
12  +4.589e-01  +4.651e-01  +3e-02  2e-06  2e-05  5e-06  1e-05  0.7667  6e-02   3  3  3 |  0  0
13  +4.584e-01  +4.601e-01  +9e-03  6e-07  6e-06  1e-06  4e-06  0.8618  1e-01   2  2  2 |  0  0
14  +4.584e-01  +4.587e-01  +2e-03  1e-07  1e-06  2e-07  7e-07  0.8522  3e-02   3  2  2 |  0  0
15  +4.584e-01  +4.584e-01  +2e-04  2e-08  1e-07  3e-08  9e-08  0.9338  8e-02   2  1  1 |  0  0
16  +4.584e-01  +4.584e-01  +2e-05  1e-09  1e-08  3e-09  7e-09  0.9189  2e-03   3  2  2 |  0  0
17  +4.584e-01  +4.584e-01  +1e-06  9e-11  8e-10  2e-10  5e-10  0.9419  1e-02   2  1  1 |  0  0
18  +4.584e-01  +4.584e-01  +7e-08  5e-12  5e-11  1e-11  3e-11  0.9423  1e-03   3  1  1 |  0  0
19  +4.584e-01  +4.584e-01  +4e-09  9e-13  3e-12  6e-13  2e-12  0.9446  5e-04   2  1  1 |  0  0

OPTIMAL (within feastol=2.8e-12, reltol=8.9e-09, abstol=4.1e-09).
Runtime: 4.596919 seconds.

Score on ham is  0.973517905507072
Score on spam is  0.9295589203423305
Sore overall is 0.959727385377943

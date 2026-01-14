<div align="center">


# **📈VocalBench: Benchmarking the Vocal Conversational Abilities for Speech Interaction Models**
<!-- # 🎧VocalNet: Speech LLM with Multi-Token Prediction for Faster and High-Quality Generation -->
<!-- <strong>English | 
[Chinese](./README_zh.md)</strong> -->

</div>

<p align="center">
HuggingFace <a href="https://huggingface.co/datasets/VocalNet/VocalBench">🤗</a> |  Paper <a href="">📖</a> 
</p>
<p align="center">
Shanghai Jiao Tong University</a>  |  Ant Group</a> 
</p>

<div align="center"><img src="images/VocalBench.png" width="25%"/></div>

## 👀 VocalBench Overview

**VocalBench** is a comprehensive evaluation benchmark to assess the vocal communication ability for speech interaction models.  

- **Semantic**: Abilities to generate accurate and vivid semantics, including knowledge, reasoning and creativity sets.
- **Acoustic**: Speech response with spontaneous and natural acoustics, evaluated on the single-round set in chat dimension.
- **Chat**: Performance on effienct and smooth chat, consisting of single- and multi-round, instruction following, emotion-aware, safety alignment sets, and a real-time factor calculation representing the computing latency.
- **Robustness**: Robustness under diverse acoustic environments, performing on white noise, background noise, reverberation, far-field, packet loss, and clipping distortion.

## 👀 News

- **2025.5**: The paper, datasets and paper of VocalBench are released, comprising systematic English conversational capability assessments.
- **2025.11**: We have extended VocalBench to include Mandarin subsets for multilingual evaluations.
- **2026.1**: We have updated the evaluation criteria, significantly expanded the model coverage, and updated the technical report.

## 🙌 Quick Start

Evaluation Scripts will be uploaded soon.


## 🏆 Leaderboard


<div align="center">
  <table style="margin: 0 auto; text-align: center;">
    <thead>
      <tr>
         <th class="tg-c3ow" colspan="15"></th>
      </tr>
    </thead>
    <tbody>
      <tr style="border-bottom: none;">
        <td rowspan="2">Model</td>
        <td>Knowledge</td>
        <td>Reasoning</td>
        <td>Creativity</td>
        <td>Fluency</td>
        <td>Clarity</td>
        <td>Single-round</td>
        <td>Multi-round</td>
        <td>Instruction Following</td>
        <td>Emotional Empathy</td>
        <td>Safety Alignment</td>
        <td colspan="2">Latency</td>
        <td>Robustness</td>
        <td rowspan="2">Overall</td>
      </tr>
      <tr>
        <td>ACC(%)</td>
        <td>ACC(%)</td>
        <td>Score</td>
        <td>UTMOS</td>
        <td>WER(%)</td>
        <td>Score</td>
        <td>ACC(%)</td>
        <td>FR(%)</td>
        <td>ERR(%)</td>
        <td>RR(%)</td>
        <td>RTF</td>
        <td>FCL</td>
        <td>PR(%)</td>
      </tr>
      <tr>
        <td colspan="14">Tiny-sized Models</td>
      </tr>
      <tr>
        <td>Mini-Omni</td>
        <td>2.25</td>
        <td>1.1</td>
        <td>1.448</td>
        <td>4.435</td>
        <td>19.571</td>
        <td>1.640</td>
        <td> - </td>
        <td>2.78</td>
        <td>21.4</td>
        <td>81.25</td>
        <td>0.3781</td>
        <td>1115.71</td>
        <td>87.631</td>
        <td>35.633</td>
      </tr>
      <tr>
        <td>Mini-Omni2</td>
        <td>4.75</td>
        <td>2.9</td>
        <td>1.828</td>
        <td>4.413</td>
        <td>36.269</td>
        <td>1.835</td>
        <td> - </td>
        <td>3.67</td>
        <td>35.8</td>
        <td>88.50</td>
        <td>0.2001</td>
        <td>911.64</td>
        <td>86.004</td>
        <td>38.201</td>
      </tr>
      <tr>
        <td>SLAM-Omni</td>
        <td>12.55</td>
        <td>9.2</td>
        <td>2.538</td>
        <td>4.424</td>
        <td>6.065</td>
        <td>3.295</td>
        <td>7.25</td>
        <td>9.33</td>
        <td>49.8</td>
        <td><b>90.25<br></td>
        <td>0.4925</td>
        <td>742.32</td>
        <td>75.356</td>
        <td>51.505</td>
      </tr>
      <tr>
        <td>VocalNet-1B</td>
        <td>46.65</td>
        <td>31.3</td>
        <td>3.425</td>
        <td><b>4.437<br></td>
        <td>5.123</td>
        <td><b>3.790<br></td>
        <td>45.50</td>
        <td>25.78</td>
        <td>46.6</td>
        <td>89.00</td>
        <td><b>0.1632<br></td>
        <td><b>414.05<br></td>
        <td>89.402</td>
        <td>64.210</td>
      </tr>
      <tr>
        <td>VocalNet2-1.7B</td>
        <td><b>47.40<br></td>
        <td><b>56.1<br></td>
        <td><b>3.493<br></td>
        <td>4.353</td>
        <td><b>1.775<br></td>
        <td>3.710</td>
        <td><b>58.00<br></td>
        <td><b>48.22<br></td>
        <td><b>51.6<br></td>
        <td>82.75</td>
        <td>0.3164</td>
        <td>673.50</td>
        <td><b>93.801<br></td>
        <td><b>71.435<br></td>
      </tr>
      <tr>
        <td colspan="14">Base-sized Models</td>
      </tr>
      <tr>
        <td>LLaMA-Omni</td>
        <td>54.70</td>
        <td>33.6</td>
        <td>3.195</td>
        <td>3.959</td>
        <td>2.842</td>
        <td>3.795</td>
        <td>48.25</td>
        <td>28.67</td>
        <td>35.4</td>
        <td>27.75</td>
        <td><b>0.0958<br></td>
        <td><b>283.19<br></td>
        <td>79.787</td>
        <td>56.919</td>
      </tr>
      <tr>
        <td>Baichuan-Omni-1.5</td>
        <td>68.65</td>
        <td>69.9</td>
        <td>3.838</td>
        <td>4.014</td>
        <td>23.452</td>
        <td>4.110</td>
        <td>-</td>
        <td>44.56</td>
        <td>23.3</td>
        <td>83.00</td>
        <td>1.4900</td>
        <td>19882.89</td>
        <td>73.080</td>
        <td>59.812</td>
      </tr>
      <tr>
        <td>Freeze-Omni</td>
        <td>62.70</td>
        <td>60.8</td>
        <td>3.380</td>
        <td>4.381</td>
        <td>11.460</td>
        <td>3.030</td>
        <td>-</td>
        <td>26.22</td>
        <td>42.2</td>
        <td>86.50</td>
        <td>0.2618</td>
        <td>557.25</td>
        <td>65.952</td>
        <td>59.936</td>
      </tr>
      <tr>
        <td>GLM-4-Voice</td>
        <td>59.85</td>
        <td>54.1</td>
        <td>3.670</td>
        <td>3.869</td>
        <td>11.565</td>
        <td>3.935</td>
        <td>65.25</td>
        <td>43.22</td>
        <td>48.2</td>
        <td>71.50</td>
        <td>0.7870</td>
        <td>1066.02</td>
        <td>57.179</td>
        <td>60.343</td>
      </tr>
      <tr>
        <td>LLaMA-Omni2-Bilingual</td>
        <td>51.60</td>
        <td>42.1</td>
        <td>3.093</td>
        <td><b>4.461<br></td>
        <td>2.744</td>
        <td>3.795</td>
        <td>62.00</td>
        <td>41.22</td>
        <td>40.2</td>
        <td>36.25</td>
        <td>0.4171</td>
        <td>1377.00</td>
        <td>83.201</td>
        <td>60.853</td>
      </tr>
      <tr>
        <td>Step-Audio-2-Mini</td>
        <td>58.90</td>
        <td>61.1</td>
        <td>3.505</td>
        <td>4.518</td>
        <td>40.069</td>
        <td>4.085</td>
        <td>58.75</td>
        <td>47.22</td>
        <td>37.0</td>
        <td>80.75</td>
        <td>5.2988</td>
        <td>1834.76</td>
        <td>84.453</td>
        <td>60.863</td>
      </tr>
      <tr>
        <td>MiniCPM-o 2.6</td>
        <td><b>75.15<br></td>
        <td>69.3</td>
        <td>3.755</td>
        <td>4.054</td>
        <td>18.735</td>
        <td>3.670</td>
        <td>65.25</td>
        <td>42.78</td>
        <td>59.8</td>
        <td>83.25</td>
        <td>0.4509</td>
        <td>1329.52</td>
        <td>83.880</td>
        <td>65.514</td>
      </tr>
      <tr>
        <td>LLaMA-Omni2</td>
        <td>59.65</td>
        <td>58.4</td>
        <td>3.145</td>
        <td>4.459</td>
        <td>3.155</td>
        <td>3.735</td>
        <td>56.00</td>
        <td>48.78</td>
        <td>42.4</td>
        <td>51.00</td>
        <td>0.4297</td>
        <td>1396.93</td>
        <td>85.746</td>
        <td>66.104</td>
      </tr>
      <tr>
        <td>Kimi-Audio</td>
        <td>72.60</td>
        <td>79.4</td>
        <td>3.640</td>
        <td>2.360</td>
        <td>38.001</td>
        <td>4.280</td>
        <td>69.75</td>
        <td><b>56.22<br></td>
        <td><b>61.1<br></td>
        <td>83.75</td>
        <td>0.7331</td>
        <td>1371.48</td>
        <td>85.620</td>
        <td>66.350</td>
      </tr>
      <tr>
        <td>VocalNet-ML</td>
        <td>61.55</td>
        <td>64.7</td>
        <td>3.345</td>
        <td>4.359</td>
        <td>5.786</td>
        <td>3.915</td>
        <td>65.50</td>
        <td>36.44</td>
        <td>59.2</td>
        <td>86.25</td>
        <td>0.2377</td>
        <td>550.07</td>
        <td><b>95.621<br></td>
        <td>72.036</td>
      </tr>
      <tr>
        <td>VITA-Audio</td>
        <td>56.15</td>
        <td>75.6</td>
        <td>3.613</td>
        <td>4.173</td>
        <td>4.858</td>
        <td>3.970</td>
        <td>-</td>
        <td>52.06</td>
        <td>49.8</td>
        <td>88.25</td>
        <td>0.4645</td>
        <td>512.64</td>
        <td>89.327</td>
        <td>72.923</td>
      </tr>
      <tr>
        <td>Qwen2.5-Omni</td>
        <td>71.00</td>
        <td>73.9</td>
        <td>3.445</td>
        <td>4.174</td>
        <td><b>1.154<br></td>
        <td>3.800</td>
        <td>71.50</td>
        <td>39.67</td>
        <td>45.2</td>
        <td>71.75</td>
        <td>1.7243</td>
        <td>-</td>
        <td>91.156</td>
        <td>72.489</td>
      </tr>
      <tr>
        <td>MiMo-Audio-Instruct</td>
        <td>67.00</td>
        <td>68.7</td>
        <td><b>4.128<br></td>
        <td>3.070</td>
        <td>5.342</td>
        <td><b>4.865<br></td>
        <td>-</td>
        <td>53.78</td>
        <td>45.3</td>
        <td>79.00</td>
        <td>0.6824</td>
        <td>-</td>
        <td>81.612</td>
        <td>72.675</td>
      </tr>
      <tr>
        <td>VocalNet-8B</td>
        <td>70.95</td>
        <td>56.3</td>
        <td>3.858</td>
        <td>4.449</td>
        <td>4.686</td>
        <td>4.125</td>
        <td>70.75</td>
        <td>45.44</td>
        <td>49.2</td>
        <td><b>92.25<br></td>
        <td>0.2496</td>
        <td>522.22</td>
        <td>91.136</td>
        <td>73.498</td>
      </tr>
      <tr>
        <td>VocalNet2-8B</td>
        <td>72.10</td>
        <td>75.0</td>
        <td>3.733</td>
        <td>4.355</td>
        <td>4.005</td>
        <td><b>4.210<br></td>
        <td>72.00</td>
        <td>53.44</td>
        <td>52.8</td>
        <td>91.50</td>
        <td>0.3860</td>
        <td>732.91</td>
        <td>92.728</td>
        <td>76.633</td>
      </tr>
      <tr>
        <td colspan="15">Large-sized Models</td>
      </tr>
      <tr>
        <td>Qwen3-Omni</td>
        <td>89.35</td>
        <td>88.5</td>
        <td>4.770</td>
        <td>4.381</td>
        <td>16.820</td>
        <td><b>4.955<br></td>
        <td>85.50</td>
        <td>72.89</td>
        <td>44.7</td>
        <td>92.25</td>
        <td>-</td>
        <td>-</td>
        <td>94.501</td>
        <td>78.775</td>
      </tr>
      <tr>
        <td colspan="15">Cascade System & Real Time API</td>
      </tr>
      <tr>
        <td>GPT Realtime</td>
        <td><b>91.80<br></td>
        <td>87.2</td>
        <td>3.970</td>
        <td>4.162</td>
        <td>6.042</td>
        <td>4.720</td>
        <td>-</td>
        <td>74.89</td>
        <td>50.0</td>
        <td>90.25</td>
        <td>-</td>
        <td>-</td>
        <td>47.872</td>
        <td>75.137</td>
      </tr>  
      <tr>
        <td>Cascade (Qwen3-8B)</td>
        <td>75.75</td>
        <td>83.9</td>
        <td>4.303</td>
        <td>4.417</td>
        <td>9.365</td>
        <td>4.900</td>
        <td>84.50</td>
        <td>71.56</td>
        <td>47.2</td>
        <td>91.50</td>
        <td>-</td>
        <td>-</td>
        <td>88.189</td>
        <td>79.041</td>
      </tr>  
      <tr>
        <td>Qwen-Omni-Turbo</td>
        <td>68.10</td>
        <td>70.2</td>
        <td>3.418</td>
        <td>4.405</td>
        <td>1.656</td>
        <td>3.705</td>
        <td>71.25</td>
        <td>40.67</td>
        <td>39.8</td>
        <td>65.25</td>
        <td>-</td>
        <td>-</td>
        <td>88.663</td>
        <td>79.351</td>
      </tr>
      <tr>
        <td>Cascade (GPT-4o)</td>
        <td>91.60</td>
        <td>86.9</td>
        <td>4.120</td>
        <td><b>4.474<br></td>
        <td>4.955</td>
        <td>4.240</td>
        <td>74.25</td>
        <td><b>77.67<br></td>
        <td>53.9</td>
        <td>91.50</td>
        <td>-</td>
        <td>-</td>
        <td>88.876</td>
        <td><b>82.682<br></td>
      </tr>  
    <thead>
      <tr>
         <th class="tg-c3ow" colspan="14"></th>
      </tr>
    </thead>
    </tbody>
  </table>
</div>


<br> 
<br> 


## 🌞 Acknowledgements

- [Whisper](https://huggingface.co/openai/whisper-large-v3): VocalBench uses Whisper for speech recognition.
- [Emotion2vec](https://huggingface.co/emotion2vec/emotion2vec_plus_large): VocalBench uses emotion2vec_plus_large for emotion recognition.
- [UTMOS](https://github.com/sarulab-speech/UTMOS22): VocalBench uses UTMOS to quantify the acoustic quality.
- [Qwen2.5-Max](https://qwenlm.github.io/blog/qwen2.5-max/): VocalBench uses Qwen2.5-Max for LLM evaluation.

<br> 
<br> 

## ⚖️ License

This repository is released under the Apache-2.0 license as found in the [LICENSE](LICENSE) file.

<br> 
<br> 

## 💡 Citation
If you find our benchmark helpful, please consider citing our papers 📝 and staring us ⭐️！

```bib
@article{liu2025vocalbench,
  title={VocalBench: Benchmarking the Vocal Conversational Abilities for Speech Interaction Models},
  author={Liu, Heyang and Wang, Yuhao and Cheng, Ziyang and Wu, Ronghua and Gu, Qunshan and Wang, Yanfeng and Wang, Yu},
  journal={arXiv preprint arXiv:2505.15727},
  year={2025}
}
```

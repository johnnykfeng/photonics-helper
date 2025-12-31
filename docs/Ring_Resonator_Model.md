# Ring Resonator With Back Reflection Model

## 1. Model Description
A ring resonator with a bus waveguide can be modelled as a system consisting of two facets with reflectivity $r$, two straight waveguides with transmission coefficient $t_{fp}$ and phases $\phi_{1}$ and $\phi_{2}$, a coupler with transmission coefficient $\sigma$, and a ring with transmission coefficient $a$, phase $\phi_{r}$, and back scattering coefficient $\rho$.

The scattering matrices ($S$) for each element describe how inputs at each port transform to outputs. Labelling the fields travelling up or right with subscript $+$ and down or left with subscript $-$, the blocks are modelled as follows:

### Facet Matrices ($S_{fp}$)
$$S_{fp}\begin{bmatrix}A_{+}\\ B_{-}\end{bmatrix}=\begin{bmatrix}A_{-}\\ B_{+}\end{bmatrix}=\begin{bmatrix}ir&t\\ t&ir\end{bmatrix}\begin{bmatrix}A_{+}\\ B_{-}\end{bmatrix}$$

$$S_{fp}\begin{bmatrix}E_{+}\\ F_{-}\end{bmatrix}=\begin{bmatrix}E_{-}\\ F_{+}\end{bmatrix}=\begin{bmatrix}ir&t\\ t&ir\end{bmatrix}\begin{bmatrix}E_{+}\\ F_{-}\end{bmatrix}$$

### Waveguide Matrices ($S_{wg}$)
$$S_{wg1}\begin{bmatrix}B_{+}\\ C_{-}\end{bmatrix}=\begin{bmatrix}B_{-}\\ C_{+}\end{bmatrix}=\begin{bmatrix}0&a_{1}\\ a_{1}&0\end{bmatrix}\begin{bmatrix}B_{+}\\ C_{-}\end{bmatrix}$$

$$S_{wg2}\begin{bmatrix}D_{+}\\ E_{-}\end{bmatrix}=\begin{bmatrix}D_{-}\\ E_{+}\end{bmatrix}=\begin{bmatrix}0&a_{2}\\ a_{2}&0\end{bmatrix}\begin{bmatrix}D_{+}\\ E_{-}\end{bmatrix}$$

### Coupler and Ring Matrices ($S_{c}, S_{r}$)
$$S_{c}\begin{bmatrix}C_{+}\\ H_{-}\\ D_{-}\\ G_{-}\end{bmatrix}=\begin{bmatrix}C_{-}\\ H_{+}\\ D_{+}\\ G_{+}\end{bmatrix}=\begin{bmatrix}0&0&\sigma&i\kappa\\ 0&0&i\kappa&\sigma\\ \sigma&i\kappa&0&0\\ i\kappa&\sigma&0&0\end{bmatrix}\begin{bmatrix}C_{+}\\ H_{-}\\ D_{-}\\ G_{-}\end{bmatrix}$$

$$S_{r}\begin{bmatrix}G_{+}\\ H_{+}\end{bmatrix}=\begin{bmatrix}G_{-}\\ H_{-}\end{bmatrix}=e^{i\phi_{r}}\begin{bmatrix}i\rho&\tau\\ \tau&i\rho^{*}\end{bmatrix}\begin{bmatrix}G_{+}\\ H_{+}\end{bmatrix}$$

### Parameter Definitions
The parameters used in the matrices are defined as:
* **Transmission:** $t=\sqrt{1-r^{2}}$.
* **Coupling:** $\kappa=\sqrt{1-\sigma^{2}}$.
* **Reflection:** $\rho=pc_{perc}\sqrt{1-\tau^{2}}e^{i\phi_{c}}$.
* **Waveguide 1:** $a_{1}=t_{fp}e^{i\phi_{1}}=t_{fp}e^{i\frac{\pi}{2}\frac{(f-f_{0})}{FSR_{fp}}+i\frac{1}{2}(\phi_{s}+\phi_{d})}$.
* **Waveguide 2:** $a_{2}=t_{fp}e^{i\phi_{2}}=t_{fp}e^{i\frac{\pi}{2}\frac{(f-f_{0})}{FSR_{fp}}+i\frac{1}{2}(\phi_{s}-\phi_{d})}$.
* **Ring Phase:** $e^{i\phi_{r}}=e^{i2\pi\frac{(f-f_{0})}{FSR_{ring}}}$.

Here, $\phi_{e}$ describes the extra phase accumulated during back reflection or the location in the ring where back reflection occurred. The phase offsets from the resonance at $f=f_{0}$ are written as a symmetric phase shared by both waveguides and the difference in phase between the two waveguides $\phi_{d}$.

---

## 2. Transmission and Reflection
The fields at each point can be solved using the linear algebra relation:
$$y=Sy+x \implies y=(I-S)^{-1}x$$

Although the solution requires the inverse of a 16x16 matrix, the matrix is sparse.

### Transmission ($T_{full}$)
To solve for transmission, let $F_{-}=0$. $F_{+}$ is solved as $A_{+}$ multiplied by a single element of the inverse matrix. Including transmission insertion loss $IL_{t}$, the full transmission is:

$$T_{full} = IL_{t}\left|\frac{t^{2}a_{1}a_{2}[(1-\sigma a_{+})(\sigma-a_{-})+(1-\sigma a_{-})(\sigma-a_{+})]/2}{(1-\sigma a_{+})(1-\sigma a_{-})+r^{2}a_{1}^{2}a_{2}^{2}(\sigma-a_{+})(\sigma-a_{-})-r(1-\sigma^{2})(a_{1}^{2}\rho+a_{2}^{2}\rho^{*})}\right|^{2}$$

**Effective Transmission Parameters:**
* $a_{\pm}=(\tau\pm i|\rho|)e^{i\phi_{r}}\triangleq ae^{\pm i\phi_{a}}e^{i\phi_{r}}$
* $|a_{\pm}|\triangleq a=\sqrt{\tau^{2}+|\rho|^{2}}$
* $\phi_{a}=arctan(\frac{|\rho|}{\tau})$

The loss from the ring is $1-a^{2}=1-\tau^{2}-|\rho|^{2}$.

**Simplified Transmission Equation:**
Defining transmission amplitude $A_{t}=IL_{t}(1-r^{2})^{2}t_{fp}^{4}$, effective reflectivity $r_{e}=rt_{fp}^{2}$, Fabry-Pérot phase $\phi_{fp}=\phi_{1}+\phi_{2}$, and phase difference $\delta=\phi_{d}+\phi_{e}$, the transmission becomes:

$$T_{full}=\frac{A_{t}}{4}\left|\frac{(1-\sigma a_{+})(\sigma-a_{-})+(1-\sigma a_{-})(\sigma-a_{+})}{(1-\sigma a_{+})(1-\sigma a_{-})+r_{e}^{2}(\sigma-a_{+})(\sigma-a_{-})e^{i2\phi_{fp}}-r_{e}(1-\sigma^{2})|\rho|e^{i(\phi_{r}+\phi_{fp})}2~cos~\delta}\right|^{2}$$

### Reflection ($R_{full}$)
Reflection is found by solving for $A_{-}$, which is a second element in the inverse matrix.
$$R_{full}=IL_{r}\left|\frac{A_{-}}{A_{+}}\right|^{2}$$

Defining reflection amplitude $A_{r}=IL_{r}/r^{2}$, the equation allows for distinguishing parameters $t_{fp}$ and $r$, meaning one extra parameter is needed for the fit.

### 2.1 Fabry-Pérot Only
Letting $\sigma=1$ (no coupling into the ring):
$$T_{fp}=\frac{A_{t}}{(1-r_{e}^{2})^{2}+4r_{e}^{2}cos^{2}(\phi_{fp})}$$

### 2.2 Ring Only
Letting $r_{e}=0$ (no back reflection at facets):
$$T_{ring}=\frac{A_{t}}{4}\left|\frac{\sigma-a_{-}}{1-\sigma a_{-}}+\frac{\sigma-a_{+}}{1-\sigma a_{+}}\right|^{2}$$

This is the sum of two Lorentzian-like functions. The extrema are:
* **Max:** $T_{L,max}=\frac{A_{t}}{4}\frac{(\sigma+a)^{2}}{(1+\sigma a)^{2}}$
* **Min:** $T_{L,min}=\frac{A_{t}}{4}\frac{(\sigma-a)^{2}}{(1-\sigma a)^{2}}$

The full width at half delta ($\Delta\phi_{FWHD}$) is:
$$\Delta\phi_{FWHD}=4~arctan\left(\frac{1-\sigma a}{1+\sigma a}\right)$$

### 2.3 Ring Only - Lorentzian Approximation
For small phase differences, the transmission can be approximated as a true Lorentzian.
$$\frac{1}{T_{1}}\approx1-\sigma a+\frac{(1-\sigma a)^{2}}{2}\approx-ln(\sigma a)$$

This approximation is valid if the Finesse $\mathcal{F} \gg 1$.

---

## 3. Derived Values

### 3.1 Critical Coupling
Critical coupling occurs when transmission at $f=f_{0}$ drops to zero. With back reflection, this can occur for a range of $\sigma$. By setting the numerator of the transmission equation to zero:
$$|\rho|=\sqrt{\frac{(\tau-\sigma)(1-\sigma\tau)}{\sigma}}$$

### 3.2 Splitting Distance
The distance between the two Lorentzian-like peaks is:
$$\Delta f=\frac{FSR_{ring}}{\pi}arctan\left(\frac{|\rho|}{\tau}\right)$$

### 3.3 Quality Factors
* **Loaded Q:** $Q_{load,m}=-\frac{\omega_{m}}{\Delta\omega_{FSR}}\frac{\pi}{ln(\sigma a)}$
* **Extrinsic Q:** $Q_{ext,m}=-\frac{\omega_{m}}{\Delta\omega_{FSR}}\frac{\pi}{ln(\sigma)}$
* **Intrinsic Q:** $Q_{int,m}=-\frac{\omega_{m}}{\Delta\omega_{FSR}}\frac{\pi}{ln(a)}$

The total dissipation rate adds harmonically:
$$\frac{1}{Q_{load,m}}=\frac{1}{Q_{int,m}}+\frac{1}{Q_{ext,m}}$$

### 3.4 Escape Efficiency
The escape efficiency is the ratio of loaded to extrinsic Q factors:
$$\eta_{esc}=\frac{Q_{load}}{Q_{ext}}=\frac{ln(\sigma)}{ln(\sigma a)}$$

---

## Appendices: Matrix Derivations

### A. Back Reflection S Matrix
The back reflection element assumes reflection occurs at one location in the ring. The reflection is allowed to be a complex number $\rho \triangleq |\rho|e^{i\phi_e}$.
$$\begin{bmatrix}A_{-}\\ D_{+}\end{bmatrix}=e^{i\phi_{r}}\begin{bmatrix}i\rho&\tau\\ \tau&i\rho^{*}\end{bmatrix}\begin{bmatrix}A_{+}\\ D_{-}\end{bmatrix}$$

### B. Transmission Minor Calculation
The determinant of the minor required for transmission ($m \triangleq |minor_{10,0}(I-S)|$) reduces to:
$$m=t^{2}a_{1}a_{2}[(1-\sigma a_{+})(\sigma-a_{-})+(1-\sigma a_{-})(\sigma-a_{+})]/2$$

### C. Reflection Minor Calculation
The determinant of the minor required for reflection ($m \triangleq |minor_{1,0}(I-S)|$) reduces to:
$$m=-ir[(1-\sigma a_{-})(1-\sigma a_{+})+a_{1}^{2}a_{2}^{2}(\sigma-a_{-})(\sigma-a_{+})-(1-\sigma^{2})(a_{1}^{2}\rho/r+ra_{2}^{2}\rho^{*})e^{i\phi_{r}}]$$

### D. Determinant Calculation
The determinant of the entire matrix ($d=|I-S|$) reduces to:
$$d=(1-\sigma a_{+})(1-\sigma a_{-})+r^{2}a_{1}^{2}a_{2}^{2}(\sigma-a_{+})(\sigma-a_{-})-r\kappa^{2}(a_{1}^{2}\rho+a_{2}^{2}\rho^{*})e^{i\phi_{r}}$$

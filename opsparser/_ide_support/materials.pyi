"""材料命令类型注解"""

from typing import overload, Literal, Optional, Any, List

class MaterialCommands:
    """材料命令的类型注解"""
    
    # === Uniaxial Materials ===
    
    # Elastic material
    @overload
    def uniaxialMaterial(self, material_type: Literal["Elastic"], material_tag: int, elastic_modulus: float, eta: Optional[float] = None) -> None:
        """Define elastic uniaxial material
        
        Args:
            material_type: Material type 'Elastic'
            material_tag: Unique material identifier
            elastic_modulus: Elastic modulus
            eta: Damping parameter (optional)
            
        Example:
            ops.uniaxialMaterial('Elastic', 1, 29000.0)
            ops.uniaxialMaterial('Elastic', 2, 29000.0, 0.01)
        """
        ...
    
    # Steel01 material
    @overload
    def uniaxialMaterial(self, material_type: Literal["Steel01"], material_tag: int, yield_strength: float, initial_stiffness: float, strain_hardening_ratio: float, a1: Optional[float] = None, a2: Optional[float] = None, a3: Optional[float] = None, a4: Optional[float] = None) -> None:
        """Define Steel01 uniaxial material with isotropic hardening
        
        Args:
            material_type: Material type 'Steel01'
            material_tag: Unique material identifier
            yield_strength: Yield strength (Fy)
            initial_stiffness: Initial elastic tangent (E0)
            strain_hardening_ratio: Strain-hardening ratio (b)
            a1, a2, a3, a4: Optional isotropic hardening parameters
            
        Example:
            ops.uniaxialMaterial('Steel01', 1, 60.0, 29000.0, 0.02)
            ops.uniaxialMaterial('Steel01', 2, 50.0, 29000.0, 0.01, 18.5, 0.925, 0.15)
        """
        ...

    # Steel02 material
    @overload
    def uniaxialMaterial(self, material_type: Literal["Steel02"], material_tag: int, Fy: float, E0: float, b: float, params: List[float], a1: Optional[float] = None, a2: Optional[float] = None, a3: Optional[float] = None, a4: Optional[float] = None, sigInit: Optional[float] = None) -> None:
        """Define Steel02 uniaxial material with Giuffre-Menegotto-Pinto model
        
        Args:
            material_type: Material type 'Steel02'
            material_tag: Unique material identifier
            Fy: Yield strength
            E0: Initial elastic tangent
            b: Strain-hardening ratio
            params: Parameters [R0, cR1, cR2] to control transition from elastic to plastic
            a1, a2, a3, a4: Optional isotropic hardening parameters
            sigInit: Initial stress value (optional)
            
        Example:
            ops.uniaxialMaterial('Steel02', 1, 60.0, 29000.0, 0.02, [20, 0.925, 0.15])
        """
        ...

    # Steel4 material  
    @overload
    def uniaxialMaterial(self, material_type: Literal["Steel4"], material_tag: int, Fy: float, E0: float, **kwargs: Any) -> None:
        """Define Steel4 uniaxial material with combined kinematic and isotropic hardening
        
        Args:
            material_type: Material type 'Steel4'
            material_tag: Unique material identifier
            Fy: Yield strength
            E0: Initial elastic tangent
            kwargs: Additional parameters for kinematic hardening (-kin), isotropic hardening (-iso), 
                   asymmetric behavior (-asym), ultimate strength (-ult), initial stress (-init), 
                   memory configuration (-mem)
            
        Example:
            ops.uniaxialMaterial('Steel4', 1, 60.0, 29000.0, '-kin', 0.02, [20, 0.90, 0.15])
        """
        ...

    # ReinforcingSteel material
    @overload  
    def uniaxialMaterial(self, material_type: Literal["ReinforcingSteel"], material_tag: int, fy: float, fu: float, Es: float, Esh: float, eps_sh: float, eps_ult: float, **kwargs: Any) -> None:
        """Define ReinforcingSteel uniaxial material for reinforced concrete
        
        Args:
            material_type: Material type 'ReinforcingSteel'
            material_tag: Unique material identifier
            fy: Yield stress in tension
            fu: Ultimate stress in tension
            Es: Initial elastic tangent
            Esh: Tangent at initial strain hardening
            eps_sh: Strain corresponding to initial strain hardening
            eps_ult: Strain at peak stress
            kwargs: Optional parameters for buckling (-GABuck, -DMBuck), fatigue (-CMFatigue), 
                   isotropic hardening (-IsoHard), curve parameters (-MPCurveParams)
            
        Example:
            ops.uniaxialMaterial('ReinforcingSteel', 1, 60.0, 90.0, 29000.0, 600.0, 0.008, 0.08)
        """
        ...

    # Dodd_Restrepo material
    @overload
    def uniaxialMaterial(self, material_type: Literal["Dodd_Restrepo"], material_tag: int, Fy: float, Fsu: float, ESH: float, ESU: float, Youngs: float, ESHI: float, FSHI: float, OmegaFac: Optional[float] = None) -> None:
        """Define Dodd-Restrepo steel material
        
        Args:
            material_type: Material type 'Dodd_Restrepo'
            material_tag: Unique material identifier
            Fy: Yield strength
            Fsu: Ultimate tensile strength (UTS)
            ESH: Tensile strain at initiation of strain hardening
            ESU: Tensile strain at the UTS
            Youngs: Modulus of elasticity
            ESHI: Tensile strain for a point on strain hardening curve
            FSHI: Tensile stress at point on strain hardening curve
            OmegaFac: Roundedness factor for Bauschinger curve (optional, default=1.0)
            
        Example:
            ops.uniaxialMaterial('Dodd_Restrepo', 1, 60.0, 90.0, 0.008, 0.08, 29000.0, 0.02, 75.0)
        """
        ...

    # RambergOsgoodSteel material
    @overload
    def uniaxialMaterial(self, material_type: Literal["RambergOsgoodSteel"], material_tag: int, fy: float, E0: float, a: float, n: float) -> None:
        """Define Ramberg-Osgood steel material
        
        Args:
            material_type: Material type 'RambergOsgoodSteel'
            material_tag: Unique material identifier
            fy: Yield strength
            E0: Initial elastic tangent
            a: Yield offset (commonly used value is 0.002)
            n: Parameter to control transition and hardening (commonly ≥ 5)
            
        Example:
            ops.uniaxialMaterial('RambergOsgoodSteel', 1, 60.0, 29000.0, 0.002, 5.0)
        """
        ...

    # SteelMPF material
    @overload
    def uniaxialMaterial(self, material_type: Literal["SteelMPF"], material_tag: int, fyp: float, fyn: float, E0: float, bp: float, bn: float, params: List[float], a1: Optional[float] = None, a2: Optional[float] = None, a3: Optional[float] = None, a4: Optional[float] = None) -> None:
        """Define SteelMPF uniaxial material with Menegotto-Pinto model
        
        Args:
            material_type: Material type 'SteelMPF'
            material_tag: Unique material identifier
            fyp: Yield strength in tension (positive loading direction)
            fyn: Yield strength in compression (negative loading direction)
            E0: Initial tangent modulus
            bp: Strain hardening ratio in tension
            bn: Strain hardening ratio in compression
            params: Parameters [R0, cR1, cR2] to control transition from elastic to plastic
            a1, a2, a3, a4: Optional isotropic hardening parameters
            
        Example:
            ops.uniaxialMaterial('SteelMPF', 1, 60.0, -60.0, 29000.0, 0.02, 0.02, [20, 0.925, 0.15])
        """
        ...

    # Steel01Thermal material
    @overload
    def uniaxialMaterial(self, material_type: Literal["Steel01Thermal"], material_tag: int, Fy: float, E0: float, b: float, a1: Optional[float] = None, a2: Optional[float] = None, a3: Optional[float] = None, a4: Optional[float] = None) -> None:
        """Define Steel01Thermal uniaxial material (thermal version of Steel01)
        
        Args:
            material_type: Material type 'Steel01Thermal'
            material_tag: Unique material identifier
            Fy: Yield strength
            E0: Initial elastic tangent
            b: Strain-hardening ratio
            a1, a2, a3, a4: Optional isotropic hardening parameters
            
        Example:
            ops.uniaxialMaterial('Steel01Thermal', 1, 60.0, 29000.0, 0.02)
        """
        ...

    # === Concrete Materials ===

    # Concrete01 material
    @overload
    def uniaxialMaterial(self, material_type: Literal["Concrete01"], material_tag: int, fpc: float, epsc0: float, fpcu: float, epsU: float) -> None:
        """Define Concrete01 uniaxial material with Kent-Scott-Park model
        
        Args:
            material_type: Material type 'Concrete01'
            material_tag: Unique material identifier
            fpc: Concrete compressive strength at 28 days (compression is negative)
            epsc0: Concrete strain at maximum strength
            fpcu: Concrete crushing strength
            epsU: Concrete strain at crushing strength
            
        Example:
            ops.uniaxialMaterial('Concrete01', 1, -4000.0, -0.002, -800.0, -0.006)
        """
        ...

    # Concrete02 material
    @overload
    def uniaxialMaterial(self, material_type: Literal["Concrete02"], material_tag: int, fpc: float, epsc0: float, fpcu: float, epsU: float, lambda_param: float, ft: float, Ets: float) -> None:
        """Define Concrete02 uniaxial material with Kent-Scott-Park model and tension
        
        Args:
            material_type: Material type 'Concrete02'
            material_tag: Unique material identifier
            fpc: Concrete compressive strength at 28 days (compression is negative)
            epsc0: Concrete strain at maximum strength
            fpcu: Concrete crushing strength
            epsU: Concrete strain at crushing strength
            lambda_param: Ratio between unloading slope at epscu and initial slope
            ft: Tensile strength
            Ets: Tension softening stiffness (absolute value)
            
        Example:
            ops.uniaxialMaterial('Concrete02', 1, -4000.0, -0.002, -800.0, -0.006, 0.1, 400.0, 2000.0)
        """
        ...

    # Concrete04 material
    @overload
    def uniaxialMaterial(self, material_type: Literal["Concrete04"], material_tag: int, fc: float, epsc: float, epscu: float, Ec: float, fct: Optional[float] = None, et: Optional[float] = None, beta: Optional[float] = None) -> None:
        """Define Concrete04 uniaxial material with Popovics model
        
        Args:
            material_type: Material type 'Concrete04'
            material_tag: Unique material identifier
            fc: Concrete compressive strength at 28 days (compression is negative)
            epsc: Concrete strain at maximum strength
            epscu: Concrete strain at crushing strength
            Ec: Initial stiffness
            fct: Maximum tensile strength of concrete (optional)
            et: Ultimate tensile strain of concrete (optional)
            beta: Exponential curve parameter to define residual stress (optional)
            
        Example:
            ops.uniaxialMaterial('Concrete04', 1, -4000.0, -0.002, -0.006, 25000.0)
        """
        ...

    # Concrete06 material
    @overload
    def uniaxialMaterial(self, material_type: Literal["Concrete06"], material_tag: int, fc: float, e0: float, n: float, k: float, alpha1: float, fcr: float, ecr: float, b: float, alpha2: float) -> None:
        """Define Concrete06 uniaxial material with tensile strength and nonlinear tension stiffening
        
        Args:
            material_type: Material type 'Concrete06'
            material_tag: Unique material identifier
            fc: Concrete compressive strength (compression is negative)
            e0: Strain at compressive strength
            n: Compressive shape factor
            k: Post-peak compressive shape factor
            alpha1: Parameter for compressive plastic strain definition
            fcr: Tensile strength
            ecr: Tensile strain at peak stress (fcr)
            b: Exponent of the tension stiffening curve
            alpha2: Parameter for tensile plastic strain definition
            
        Example:
            ops.uniaxialMaterial('Concrete06', 1, -4000.0, -0.002, 2.0, 1.0, 0.08, 400.0, 0.0001, 0.1, 0.08)
        """
        ...

    # Concrete07 material
    @overload
    def uniaxialMaterial(self, material_type: Literal["Concrete07"], material_tag: int, fc: float, epsc: float, Ec: float, ft: float, et: float, xp: float, xn: float, r: float) -> None:
        """Define Concrete07 uniaxial material based on Chang & Mander model
        
        Args:
            material_type: Material type 'Concrete07'
            material_tag: Unique material identifier
            fc: Concrete compressive strength (compression is negative)
            epsc: Concrete strain at maximum compressive strength
            Ec: Initial elastic modulus of the concrete
            ft: Tensile strength of concrete (tension is positive)
            et: Tensile strain at max tensile strength of concrete
            xp: Non-dimensional term defining strain at which straight line descent begins in tension
            xn: Non-dimensional term defining strain at which straight line descent begins in compression
            r: Parameter that controls the nonlinear descending branch
            
        Example:
            ops.uniaxialMaterial('Concrete07', 1, -4000.0, -0.002, 25000.0, 400.0, 0.0001, 10000.0, 2.0, 4.0)
        """
        ...

    # Concrete01WithSITC material
    @overload
    def uniaxialMaterial(self, material_type: Literal["Concrete01WithSITC"], material_tag: int, fpc: float, epsc0: float, fpcu: float, epsU: float, endStrainSITC: Optional[float] = None) -> None:
        """Define Concrete01WithSITC uniaxial material with Stuff In The Cracks effect
        
        Args:
            material_type: Material type 'Concrete01WithSITC'
            material_tag: Unique material identifier
            fpc: Concrete compressive strength at 28 days (compression is negative)
            epsc0: Concrete strain at maximum strength
            fpcu: Concrete crushing strength
            epsU: Concrete strain at crushing strength
            endStrainSITC: End strain for SITC effect (optional, default=0.03)
            
        Example:
            ops.uniaxialMaterial('Concrete01WithSITC', 1, -4000.0, -0.002, -800.0, -0.006)
        """
        ...

    # ConfinedConcrete01 material
    @overload
    def uniaxialMaterial(self, material_type: Literal["ConfinedConcrete01"], material_tag: int, secType: str, fpc: float, Ec: float, epscu_type: str, epscu_val: float, **kwargs: Any) -> None:
        """Define ConfinedConcrete01 uniaxial material for confined concrete
        
        Args:
            material_type: Material type 'ConfinedConcrete01'
            material_tag: Unique material identifier
            secType: Section type ('S1', 'S2', 'S3', 'S4a', 'S4b', 'S5', 'C', 'R')
            fpc: Unconfined cylindrical strength of concrete specimen
            Ec: Initial elastic modulus of unconfined concrete
            epscu_type: Method to define ultimate strain ('-epscu' or '-gamma')
            epscu_val: Value for ultimate strain definition
            kwargs: Additional parameters for geometry, reinforcement, wrapping, etc.
            
        Example:
            ops.uniaxialMaterial('ConfinedConcrete01', 1, 'C', -30.0, 25000.0, '-epscu', 0.05)
        """
        ...

    # ConcreteD material
    @overload
    def uniaxialMaterial(self, material_type: Literal["ConcreteD"], material_tag: int, fc: float, epsc: float, ft: float, epst: float, Ec: float, alphac: float, alphat: float, cesp: Optional[float] = None, etap: Optional[float] = None) -> None:
        """Define ConcreteD uniaxial material based on Chinese design code
        
        Args:
            material_type: Material type 'ConcreteD'
            material_tag: Unique material identifier
            fc: Concrete compressive strength
            epsc: Concrete strain at compressive strength
            ft: Concrete tensile strength
            epst: Concrete strain at tensile strength
            Ec: Concrete initial elastic modulus
            alphac: Compressive descending parameter
            alphat: Tensile descending parameter
            cesp: Plastic parameter (optional, recommended 0.2~0.3, default=0.25)
            etap: Plastic parameter (optional, recommended 1.0~1.3, default=1.15)
            
        Example:
            ops.uniaxialMaterial('ConcreteD', 1, -30.0, -0.002, 3.0, 0.0001, 30000.0, 2.0, 1.5)
        """
        ...

    # FRPConfinedConcrete material
    @overload
    def uniaxialMaterial(self, material_type: Literal["FRPConfinedConcrete"], material_tag: int, fpc1: float, fpc2: float, epsc0: float, D: float, c: float, Ej: float, Sj: float, tj: float, eju: float, S: float, fyl: float, fyh: float, dlong: float, dtrans: float, Es: float, nu0: float, k: float, useBuck: float) -> None:
        """Define FRPConfinedConcrete uniaxial material
        
        Args:
            material_type: Material type 'FRPConfinedConcrete'
            material_tag: Unique material identifier
            fpc1: Concrete core compressive strength
            fpc2: Concrete cover compressive strength
            epsc0: Strain corresponding to unconfined concrete strength
            D: Diameter of the circular section
            c: Dimension of concrete cover
            Ej: Elastic modulus of the FRP jacket
            Sj: Clear spacing of the FRP strips
            tj: Total thickness of the FRP jacket
            eju: Rupture strain of the FRP jacket from tensile coupons
            S: Spacing of the steel spiral/stirrups
            fyl: Yielding strength of longitudinal steel bars
            fyh: Yielding strength of the steel spiral/stirrups
            dlong: Diameter of the longitudinal bars
            dtrans: Diameter of the steel spiral/stirrups
            Es: Elastic modulus of steel
            nu0: Initial Poisson's coefficient for concrete
            k: Reduction factor for the rupture strain of the FRP jacket
            useBuck: FRP jacket failure criterion due to buckling
            
        Example:
            ops.uniaxialMaterial('FRPConfinedConcrete', 1, 30.0, 25.0, 0.002, 300.0, 25.0, 230000.0, 0.0, 1.0, 0.012, 100.0, 400.0, 600.0, 16.0, 8.0, 200000.0, 0.2, 0.75, 1.0)
        """
        ...

    # FRPConfinedConcrete02 material
    @overload
    def uniaxialMaterial(self, material_type: Literal["FRPConfinedConcrete02"], material_tag: int, fc0: float, Ec: float, ec0: float, ft: float, Ets: float, Unit: float, **kwargs: Any) -> None:
        """Define FRPConfinedConcrete02 uniaxial hysteretic material
        
        Args:
            material_type: Material type 'FRPConfinedConcrete02'
            material_tag: Unique material identifier
            fc0: Compressive strength of unconfined concrete (compression is negative)
            Ec: Elastic modulus of unconfined concrete
            ec0: Axial strain corresponding to unconfined concrete strength
            ft: Tensile strength of unconfined concrete
            Ets: Stiffness of tensile softening
            Unit: Unit indicator (1 for SI Metric Units, 0 for US Customary Units)
            kwargs: Optional parameters for FRP jacket (-JacketC) or ultimate values (-Ultimate)
            
        Example:
            ops.uniaxialMaterial('FRPConfinedConcrete02', 1, -30.0, 25000.0, -0.002, 3.0, 1250.0, 1)
        """
        ...

    # ConcreteCM material
    @overload
    def uniaxialMaterial(self, material_type: Literal["ConcreteCM"], material_tag: int, fpcc: float, epcc: float, Ec: float, rc: float, xcrn: float, ft: float, et: float, rt: float, xcrp: float, mon: int, GapClose: Optional[int] = None) -> None:
        """Define ConcreteCM uniaxial hysteretic material
        
        Args:
            material_type: Material type 'ConcreteCM'
            material_tag: Unique material identifier
            fpcc: Compressive strength
            epcc: Strain at compressive strength
            Ec: Initial tangent modulus
            rc: Shape parameter in Tsai's equation for compression
            xcrn: Non-dimensional critical strain on compression envelope
            ft: Tensile strength
            et: Strain at tensile strength
            rt: Shape parameter in Tsai's equation for tension
            xcrp: Non-dimensional critical strain on tension envelope
            mon: Monotonic stress-strain relationship (1 for monotonic, 0 for cyclic)
            GapClose: Gap closure parameter (optional, 0 for less gradual, 1 for more gradual)
            
        Example:
            ops.uniaxialMaterial('ConcreteCM', 1, -30.0, -0.002, 25000.0, 7.0, 3.0, 3.0, 0.0001, 1.2, 10000.0, 0)
        """
        ...

    # TDConcrete material
    @overload
    def uniaxialMaterial(self, material_type: Literal["TDConcrete"], material_tag: int, fc: float, fct: float, Ec: float, beta: float, tD: float, epsshu: float, psish: float, Tcr: float, phiu: float, psicr1: float, psicr2: float, tcast: float) -> None:
        """Define TDConcrete time-dependent uniaxial material
        
        Args:
            material_type: Material type 'TDConcrete'
            material_tag: Unique material identifier
            fc: Concrete compressive strength (compression is negative)
            fct: Concrete tensile strength (tension is positive)
            Ec: Concrete modulus of elasticity
            beta: Tension softening parameter
            tD: Analysis time at initiation of drying (in days)
            epsshu: Ultimate shrinkage strain as per ACI 209R-92 (shrinkage is negative)
            psish: Fitting parameter of the shrinkage time evolution function
            Tcr: Creep model age (in days)
            phiu: Ultimate creep coefficient as per ACI 209R-92
            psicr1: Fitting parameter of the creep time evolution function
            psicr2: Fitting parameter of the creep time evolution function
            tcast: Analysis time corresponding to concrete casting (in days, minimum 2.0)
            
        Example:
            ops.uniaxialMaterial('TDConcrete', 1, -30.0, 3.0, 25000.0, 0.1, 7.0, -0.0003, 0.5, 28.0, 2.35, 10.0, 5.0, 1.0)
        """
        ...

    # TDConcreteEXP material
    @overload
    def uniaxialMaterial(self, material_type: Literal["TDConcreteEXP"], material_tag: int, fc: float, fct: float, Ec: float, beta: float, tD: float, epsshu: float, psish: float, Tcr: float, epscru: float, sigCr: float, psicr1: float, psicr2: float, tcast: float) -> None:
        """Define TDConcreteEXP time-dependent uniaxial material with experimental creep
        
        Args:
            material_type: Material type 'TDConcreteEXP'
            material_tag: Unique material identifier
            fc: Concrete compressive strength (compression is negative)
            fct: Concrete tensile strength (tension is positive)
            Ec: Concrete modulus of elasticity
            beta: Tension softening parameter
            tD: Analysis time at initiation of drying (in days)
            epsshu: Ultimate shrinkage strain as per ACI 209R-92 (shrinkage is negative)
            psish: Fitting parameter of the shrinkage time evolution function
            Tcr: Creep model age (in days)
            epscru: Ultimate creep strain (from experimental measurements)
            sigCr: Concrete compressive stress associated with epscru (input as negative)
            psicr1: Fitting parameter of the creep time evolution function
            psicr2: Fitting parameter of the creep time evolution function
            tcast: Analysis time corresponding to concrete casting (in days, minimum 2.0)
            
        Example:
            ops.uniaxialMaterial('TDConcreteEXP', 1, -30.0, 3.0, 25000.0, 0.1, 7.0, -0.0003, 0.5, 28.0, -0.001, -15.0, 10.0, 5.0, 1.0)
        """
        ...

    # TDConcreteMC10 material
    @overload
    def uniaxialMaterial(self, material_type: Literal["TDConcreteMC10"], material_tag: int, fc: float, fct: float, Ec: float, Ecm: float, beta: float, tD: float, epsba: float, epsbb: float, epsda: float, epsdb: float, phiba: float, phibb: float, phida: float, phidb: float, tcast: float, cem: float) -> None:
        """Define TDConcreteMC10 time-dependent material according to fib Model Code 2010
        
        Args:
            material_type: Material type 'TDConcreteMC10'
            material_tag: Unique material identifier
            fc: Concrete compressive strength (compression is negative)
            fct: Concrete tensile strength (tension is positive)
            Ec: Concrete modulus of elasticity at loading age
            Ecm: Concrete modulus of elasticity at 28 days
            beta: Tension softening parameter
            tD: Analysis time at initiation of drying (in days)
            epsba: Ultimate basic shrinkage strain (input as negative)
            epsbb: Fitting parameter of the basic shrinkage time evolution function
            epsda: Product of ultimate drying shrinkage strain and relative humidity function
            epsdb: Fitting parameter of the basic shrinkage time evolution function
            phiba: Parameter for the effect of compressive strength on basic creep
            phibb: Fitting parameter of the basic creep time evolution function
            phida: Product of the effect of compressive strength and relative humidity on drying creep
            phidb: Fitting parameter of the drying creep time evolution function
            tcast: Analysis time corresponding to concrete casting (in days, minimum 2.0)
            cem: Coefficient dependent on the type of cement
            
        Example:
            ops.uniaxialMaterial('TDConcreteMC10', 1, -30.0, 3.0, 25000.0, 30000.0, 0.1, 7.0, -0.0001, 1.0, -0.0002, 0.5, 1.8, 0.3, 2.3, 1.0, 1.0, 1.0)
        """
        ...

    # TDConcreteMC10NL material
    @overload
    def uniaxialMaterial(self, material_type: Literal["TDConcreteMC10NL"], material_tag: int, fc: float, fcu: float, epscu: float, fct: float, Ec: float, Ecm: float, beta: float, tD: float, epsba: float, epsbb: float, epsda: float, epsdb: float, phiba: float, phibb: float, phida: float, phidb: float, tcast: float, cem: float) -> None:
        """Define TDConcreteMC10NL time-dependent material with non-linear compression
        
        Args:
            material_type: Material type 'TDConcreteMC10NL'
            material_tag: Unique material identifier
            fc: Concrete compressive strength (compression is negative)
            fcu: Concrete crushing strength (compression is negative)
            epscu: Concrete strain at crushing strength (input as negative)
            fct: Concrete tensile strength (tension is positive)
            Ec: Concrete modulus of elasticity at loading age
            Ecm: Concrete modulus of elasticity at 28 days
            beta: Tension softening parameter
            tD: Analysis time at initiation of drying (in days)
            epsba: Ultimate basic shrinkage strain (input as negative)
            epsbb: Fitting parameter of the basic shrinkage time evolution function
            epsda: Product of ultimate drying shrinkage strain and relative humidity function
            epsdb: Fitting parameter of the basic shrinkage time evolution function
            phiba: Parameter for the effect of compressive strength on basic creep
            phibb: Fitting parameter of the basic creep time evolution function
            phida: Product of the effect of compressive strength and relative humidity on drying creep
            phidb: Fitting parameter of the drying creep time evolution function
            tcast: Analysis time corresponding to concrete casting (in days, minimum 2.0)
            cem: Coefficient dependent on the type of cement
            
        Example:
            ops.uniaxialMaterial('TDConcreteMC10NL', 1, -30.0, -6.0, -0.005, 3.0, 25000.0, 30000.0, 0.1, 7.0, -0.0001, 1.0, -0.0002, 0.5, 1.8, 0.3, 2.3, 1.0, 1.0, 1.0)
        """
        ...

    # Generic uniaxial material fallback
    @overload
    def uniaxialMaterial(self, material_type: str, material_tag: int, *args: Any) -> None:
        """Define uniaxial material (generic fallback)
        
        Args:
            material_type: Material type
            material_tag: Unique material identifier
            args: Material properties
            
        Example:
            ops.uniaxialMaterial('SomeOtherMaterial', 1, ...)
        """
        ...

    # Generic nD material fallback
    @overload
    def nDMaterial(self, material_type: str, material_tag: int, *args: Any) -> None:
        """Define nD material (generic fallback)
        
        Args:
            material_type: Material type
            material_tag: Unique material identifier
            args: Material properties
            
        Example:
            ops.nDMaterial('SomeOtherMaterial', 1, ...)
        """
        ... 
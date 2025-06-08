"""材料命令类型注解"""

from typing import overload, Literal, Optional, Any

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
    def uniaxialMaterial(self, material_type: Literal["Steel02"], material_tag: int, yield_strength: float, initial_stiffness: float, strain_hardening_ratio: float, control_params: Literal["R0", "cR1", "cR2"], r0: float, cr1: float, cr2: float, a1: Optional[float] = None, a2: Optional[float] = None, a3: Optional[float] = None, a4: Optional[float] = None, sig_init: Optional[float] = None) -> None:
        """Define Steel02 uniaxial material with Giuffré-Menegotto-Pinto model
        
        Args:
            material_type: Material type 'Steel02'
            material_tag: Unique material identifier
            yield_strength: Yield strength (Fy)
            initial_stiffness: Initial elastic tangent (E0)
            strain_hardening_ratio: Strain-hardening ratio (b)
            control_params: Control parameter type
            r0: Control of transition from elastic to plastic branches
            cr1, cr2: Control of transition from elastic to plastic branches
            a1, a2, a3, a4: Isotropic hardening parameters
            sig_init: Initial stress
            
        Example:
            ops.uniaxialMaterial('Steel02', 1, 60.0, 29000.0, 0.02, 'R0', 20.0, 0.9, 0.1)
        """
        ...
    
    # Concrete01 material
    @overload
    def uniaxialMaterial(self, material_type: Literal["Concrete01"], material_tag: int, compressive_strength: float, strain_at_fc: float, crushing_strength: float, strain_at_fcu: float) -> None:
        """Define Concrete01 uniaxial material with zero tensile strength
        
        Args:
            material_type: Material type 'Concrete01'
            material_tag: Unique material identifier
            compressive_strength: Compressive strength (fc, negative value)
            strain_at_fc: Strain at compressive strength (ec0, negative value)
            crushing_strength: Crushing strength (fcu, negative value)
            strain_at_fcu: Strain at crushing strength (ecu, negative value)
            
        Example:
            ops.uniaxialMaterial('Concrete01', 1, -4000.0, -0.002, -1000.0, -0.006)
        """
        ...
    
    # Concrete02 material
    @overload
    def uniaxialMaterial(self, material_type: Literal["Concrete02"], material_tag: int, compressive_strength: float, strain_at_fc: float, crushing_strength: float, strain_at_fcu: float, lambda_param: float, tensile_strength: float, tension_stiffening: float) -> None:
        """Define Concrete02 uniaxial material with linear tension softening
        
        Args:
            material_type: Material type 'Concrete02'
            material_tag: Unique material identifier
            compressive_strength: Compressive strength (fc, negative value)
            strain_at_fc: Strain at compressive strength (ec0, negative value)
            crushing_strength: Crushing strength (fcu, negative value)
            strain_at_fcu: Strain at crushing strength (ecu, negative value)
            lambda_param: Ratio between unloading slope at εcu and initial slope
            tensile_strength: Tensile strength (ft)
            tension_stiffening: Tension stiffening parameter
            
        Example:
            ops.uniaxialMaterial('Concrete02', 1, -4000.0, -0.002, -1000.0, -0.006, 0.1, 400.0, 0.4)
        """
        ...
    
    # Hysteretic material
    @overload
    def uniaxialMaterial(self, material_type: Literal["Hysteretic"], material_tag: int, *points_and_params: float) -> None:
        """Define Hysteretic uniaxial material
        
        Args:
            material_type: Material type 'Hysteretic'
            material_tag: Unique material identifier
            points_and_params: Stress-strain points and hysteretic parameters
            
        Example:
            ops.uniaxialMaterial('Hysteretic', 1, 60.0, 0.002, 80.0, 0.02, 10.0, 0.08, -60.0, -0.002, -80.0, -0.02, -10.0, -0.08, 1.0, 1.0, 0.0, 0.0)
        """
        ...
    
    # MinMax material
    @overload
    def uniaxialMaterial(self, material_type: Literal["MinMax"], material_tag: int, other_material_tag: int, min_strain: Optional[float] = None, max_strain: Optional[float] = None) -> None:
        """Define MinMax wrapper material
        
        Args:
            material_type: Material type 'MinMax'
            material_tag: Unique material identifier
            other_material_tag: Tag of wrapped material
            min_strain: Minimum strain (optional)
            max_strain: Maximum strain (optional)
            
        Example:
            ops.uniaxialMaterial('MinMax', 1, 2, -0.01, 0.02)
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
    
    # === nD Materials ===
    
    # Elastic isotropic material
    @overload
    def nDMaterial(self, material_type: Literal["ElasticIsotropic"], material_tag: int, elastic_modulus: float, poisson_ratio: float, density: Optional[float] = None) -> None:
        """Define elastic isotropic nD material
        
        Args:
            material_type: Material type 'ElasticIsotropic'
            material_tag: Unique material identifier
            elastic_modulus: Elastic modulus
            poisson_ratio: Poisson's ratio
            density: Mass density (optional)
            
        Example:
            ops.nDMaterial('ElasticIsotropic', 1, 29000.0, 0.3)
            ops.nDMaterial('ElasticIsotropic', 2, 29000.0, 0.3, 0.000283)
        """
        ...
    
    # J2 plasticity material
    @overload
    def nDMaterial(self, material_type: Literal["J2Plasticity"], material_tag: int, elastic_modulus: float, poisson_ratio: float, yield_stress: float, kinematic_hardening: float, isotropic_hardening: float, density: Optional[float] = None) -> None:
        """Define J2 plasticity nD material
        
        Args:
            material_type: Material type 'J2Plasticity'
            material_tag: Unique material identifier
            elastic_modulus: Elastic modulus
            poisson_ratio: Poisson's ratio
            yield_stress: Initial yield stress
            kinematic_hardening: Kinematic hardening parameter
            isotropic_hardening: Isotropic hardening parameter
            density: Mass density (optional)
            
        Example:
            ops.nDMaterial('J2Plasticity', 1, 29000.0, 0.3, 60.0, 0.0, 0.0)
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
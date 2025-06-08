"""单元命令类型注解"""

from typing import overload, Literal, Any

class ElementCommands:
    """单元命令的类型注解"""
    
    # Truss elements
    @overload
    def element(self, element_type: Literal["truss"], element_tag: int, node_i: int, node_j: int, area: float, material_tag: int) -> None:
        """Create truss element
        
        Args:
            element_type: Element type 'truss'
            element_tag: Unique element identifier
            node_i: Start node tag
            node_j: End node tag
            area: Cross-sectional area
            material_tag: Material tag
            
        Example:
            ops.element('truss', 1, 1, 2, 100.0, 1)
        """
        ...
    
    # Elastic beam-column elements
    @overload
    def element(self, element_type: Literal["elasticBeamColumn"], element_tag: int, node_i: int, node_j: int, area: float, elastic_modulus: float, moment_of_inertia: float, geom_transf_tag: int) -> None:
        """Create elastic beam-column element
        
        Args:
            element_type: Element type 'elasticBeamColumn'
            element_tag: Unique element identifier
            node_i: Start node tag
            node_j: End node tag
            area: Cross-sectional area
            elastic_modulus: Elastic modulus
            moment_of_inertia: Moment of inertia
            geom_transf_tag: Geometric transformation tag
            
        Example:
            ops.element('elasticBeamColumn', 2, 1, 2, 100.0, 29000.0, 1000.0, 1)
        """
        ...
    
    # Displacement-based beam-column elements
    @overload
    def element(self, element_type: Literal["dispBeamColumn"], element_tag: int, node_i: int, node_j: int, geom_transf_tag: int, integration_type: str, section_tag: int, num_integration_points: int) -> None:
        """Create displacement-based beam-column element
        
        Args:
            element_type: Element type 'dispBeamColumn'
            element_tag: Unique element identifier
            node_i: Start node tag
            node_j: End node tag
            geom_transf_tag: Geometric transformation tag
            integration_type: Integration type ('Lobatto', 'Legendre', etc.)
            section_tag: Section tag
            num_integration_points: Number of integration points
            
        Example:
            ops.element('dispBeamColumn', 3, 1, 2, 1, 'Lobatto', 1, 5)
        """
        ...
    
    # Nonlinear beam-column elements
    @overload  
    def element(self, element_type: Literal["nonlinearBeamColumn"], element_tag: int, node_i: int, node_j: int, num_integration_points: int, section_tag: int, geom_transf_tag: int) -> None:
        """Create nonlinear beam-column element with fiber section
        
        Args:
            element_type: Element type 'nonlinearBeamColumn'
            element_tag: Unique element identifier
            node_i: Start node tag
            node_j: End node tag
            num_integration_points: Number of integration points
            section_tag: Section tag
            geom_transf_tag: Geometric transformation tag
            
        Example:
            ops.element('nonlinearBeamColumn', 4, 1, 2, 5, 1, 1)
        """
        ...
    
    # Quad elements
    @overload
    def element(self, element_type: Literal["quad"], element_tag: int, node1: int, node2: int, node3: int, node4: int, thickness: float, material_type: str, material_tag: int, *additional_params: float) -> None:
        """Create quad element
        
        Args:
            element_type: Element type 'quad'
            element_tag: Unique element identifier
            node1, node2, node3, node4: Corner node tags (counterclockwise)
            thickness: Element thickness
            material_type: Material type ('PlaneStrain', 'PlaneStress', etc.)
            material_tag: Material tag
            additional_params: Additional material parameters
            
        Example:
            ops.element('quad', 5, 1, 2, 3, 4, 0.1, 'PlaneStrain', 1)
        """
        ...
    
    # Shell elements
    @overload
    def element(self, element_type: Literal["shellMITC4"], element_tag: int, node1: int, node2: int, node3: int, node4: int, section_tag: int) -> None:
        """Create shell MITC4 element
        
        Args:
            element_type: Element type 'shellMITC4'
            element_tag: Unique element identifier
            node1, node2, node3, node4: Corner node tags
            section_tag: Section tag
            
        Example:
            ops.element('shellMITC4', 6, 1, 2, 3, 4, 1)
        """
        ...
    
    # Zero-length elements
    @overload
    def element(self, element_type: Literal["zeroLength"], element_tag: int, node_i: int, node_j: int, material_flag: Literal["-mat"], *material_data: int) -> None:
        """Create zero-length element
        
        Args:
            element_type: Element type 'zeroLength'
            element_tag: Unique element identifier
            node_i: Start node tag
            node_j: End node tag
            material_flag: Flag '-mat'
            material_data: Material tags and DOF directions
            
        Example:
            ops.element('zeroLength', 7, 1, 2, '-mat', 1, '-dir', 1)
        """
        ...
    
    # Spring elements
    @overload
    def element(self, element_type: Literal["twoNodeLink"], element_tag: int, node_i: int, node_j: int, material_flag: Literal["-mat"], *material_data: int) -> None:
        """Create two-node link element
        
        Args:
            element_type: Element type 'twoNodeLink'
            element_tag: Unique element identifier
            node_i: Start node tag
            node_j: End node tag
            material_flag: Flag '-mat'
            material_data: Material tags and DOF directions
            
        Example:
            ops.element('twoNodeLink', 8, 1, 2, '-mat', 1, '-dir', 1)
        """
        ...
    
    # Generic fallback
    @overload
    def element(self, element_type: str, element_tag: int, *args: Any) -> None:
        """Create element (generic fallback)
        
        Args:
            element_type: Element type
            element_tag: Unique element identifier
            args: Element parameters
            
        Example:
            ops.element('someOtherElement', 1, 1, 2, ...)
        """
        ... 
"""几何变换命令类型注解"""

from typing import overload, Literal, Optional, Any

class GeometryCommands:
    """几何变换命令的类型注解"""
    
    # Linear transformation
    @overload  
    def geomTransf(self, transf_type: Literal["Linear"], transf_tag: int, vec_x_z: Optional[float] = None, vec_y_z: Optional[float] = None, vec_z_z: Optional[float] = None) -> None:
        """Define linear coordinate transformation
        
        Args:
            transf_type: Transformation type 'Linear'
            transf_tag: Unique transformation identifier  
            vec_x_z, vec_y_z, vec_z_z: Vector components defining local-z axis (3D only)
            
        Example:
            ops.geomTransf('Linear', 1)                    # 2D transformation
            ops.geomTransf('Linear', 2, 0.0, 0.0, 1.0)     # 3D transformation
        """
        ...
    
    # P-Delta transformation
    @overload
    def geomTransf(self, transf_type: Literal["PDelta"], transf_tag: int, vec_x_z: Optional[float] = None, vec_y_z: Optional[float] = None, vec_z_z: Optional[float] = None) -> None:
        """Define P-Delta coordinate transformation
        
        Args:
            transf_type: Transformation type 'PDelta'
            transf_tag: Unique transformation identifier
            vec_x_z, vec_y_z, vec_z_z: Vector components defining local-z axis (3D only)
            
        Example:
            ops.geomTransf('PDelta', 1)                    # 2D P-Delta transformation
            ops.geomTransf('PDelta', 2, 0.0, 0.0, 1.0)     # 3D P-Delta transformation
        """
        ...
    
    # Corotational transformation
    @overload
    def geomTransf(self, transf_type: Literal["Corotational"], transf_tag: int, vec_x_z: Optional[float] = None, vec_y_z: Optional[float] = None, vec_z_z: Optional[float] = None) -> None:
        """Define corotational coordinate transformation
        
        Args:
            transf_type: Transformation type 'Corotational'
            transf_tag: Unique transformation identifier
            vec_x_z, vec_y_z, vec_z_z: Vector components defining local-z axis (3D only)
            
        Example:
            ops.geomTransf('Corotational', 1)              # 2D corotational transformation
            ops.geomTransf('Corotational', 2, 0.0, 0.0, 1.0) # 3D corotational transformation
        """
        ...
    
    # Generic transformation fallback
    @overload
    def geomTransf(self, transf_type: str, transf_tag: int, *args: Any) -> None:
        """Define coordinate transformation (generic fallback)
        
        Args:
            transf_type: Transformation type
            transf_tag: Unique transformation identifier
            args: Transformation parameters
            
        Example:
            ops.geomTransf('SomeOtherTransf', 1, ...)
        """
        ... 
from typing import Any, Dict, List, Optional, Set, Union
import math

from ._Selector import Selector, SelectType, MaterialSelectItem, MaterialProperty

class MaterialSelector(Selector):
    """Material selector implementing functionality similar to ANSYS MP command"""
    
    def _select_new(self,
                   item: MaterialSelectItem = None,
                   comp: str = None,
                   vmin: Union[int, float, str] = None,
                   vmax: Union[int, float, str] = None,
                   vinc: int = 1,
                   kabs: int = 0,
                   **kwargs) -> Set[int]:
        """
        Create new material selection based on criteria
        
        Args:
            item: Selection item type
            comp: Component for selection
            vmin: Minimum value
            vmax: Maximum value
            vinc: Value increment
            kabs: Absolute value key (0=Check sign, 1=Use absolute value)
            **kwargs: Additional selection criteria
            
        Returns:
            Set of selected material IDs
        """
        if not item:
            return set()
            
        vmax = vmax if vmax is not None else vmin
        selected = set()
        
        # Select by material ID
        if item == MaterialSelectItem.TAG.value:
            if isinstance(vmin, (int, float)):
                selected = {mid for mid in self._items.keys() 
                          if vmin <= mid <= vmax and (mid - vmin) % vinc == 0}
                          
        # Select by material type
        elif item == MaterialSelectItem.TYPE.value:
            for mid, mat in self._items.items():
                if vmin <= mat.get('type', 0) <= vmax:
                    selected.add(mid)
                    
        # Select by material category
        elif item == MaterialSelectItem.CATEGORY.value:
            for mid, mat in self._items.items():
                if mat.get('category', '') == vmin:
                    selected.add(mid)
                    
        # Select by property
        elif item == MaterialSelectItem.PROPERTY.value:
            if not comp or not isinstance(comp, MaterialProperty):
                return set()
                
            for mid, mat in self._items.items():
                props = mat.get('properties', {})
                if comp.value in props:
                    val = abs(props[comp.value]) if kabs else props[comp.value]
                    if vmin <= val <= vmax:
                        selected.add(mid)
                        
 
        return selected
        
    def get_types(self) -> List[int]:
        """Get types of selected materials"""
        return [mat.get('type', 0) for mat in self]
        
    def get_categories(self) -> List[str]:
        """Get categories of selected materials"""
        return [mat.get('category', '') for mat in self]
        
    def get_properties(self) -> List[Dict[str, float]]:
        """Get properties of selected materials"""
        return [mat.get('properties', {}) for mat in self]
        
    def used_by_elements(self) -> List[List[int]]:
        """Get elements using selected materials"""
        if not self._element_manager:
            return []
            
        result = []
        for mat_id in self._current_selection:
            elements = self._element_manager.get_elements_by_material(mat_id)
            result.append(elements)
        return result 
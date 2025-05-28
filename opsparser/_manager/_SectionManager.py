from typing import Any, Optional, Dict, List

from ._BaseHandler import BaseHandler


class SectionManager(BaseHandler):
    """Manager for section commands in OpenSeesPy
    
    Handles section command which creates SectionForceDeformation objects
    representing force-deformation relationships at beam-column and plate sample points.
    """
    
    def __init__(self):
        self.sections = {}  # tag -> section_info
        
    @property
    def _COMMAND_RULES(self) -> dict[str, dict[str, Any]]:
        """Define parsing rules for section commands"""
        return {
            # section(secType, secTag, *secArgs)
            "section": {
                "positional": ["sec_type", "tag", "args*"],
                "options": {
                    "-GJ?": "GJ",
                    "-torsion?": "torsion_mat_tag",
                    "-ndf?": "ndf",
                },
            },
        }
    
    def handles(self) -> List[str]:
        """Return list of commands this manager handles"""
        return ["section"]
    
    def handle(self, func_name: str, arg_map: dict[str, Any]):
        """Handle section commands"""
        if func_name == "section":
            args, kwargs = arg_map.get("args"), arg_map.get("kwargs")
            parsed_args = self._parse("section", *args, **kwargs)
            self._handle_section(parsed_args)
    
    def _handle_section(self, arg_map: dict[str, Any]):
        """Handle section command
        
        Args:
            arg_map: Parsed arguments from _parse method
        """
        sec_type = arg_map.get("sec_type")
        tag = arg_map.get("tag")
        
        if not sec_type or tag is None:
            return
            
        # Extract section-specific arguments
        args = arg_map.get("args", [])
        section_info = {
            "type": sec_type,
            "tag": tag,
            "args": args,
        }
        
        # Handle optional parameters
        if "GJ" in arg_map:
            section_info["GJ"] = arg_map["GJ"]
        if "torsion_mat_tag" in arg_map:
            section_info["torsion_mat_tag"] = arg_map["torsion_mat_tag"]
        if "ndf" in arg_map:
            section_info["ndf"] = arg_map["ndf"]
            
        # Store section information
        self.sections[tag] = section_info
    
    def get_section(self, tag: int) -> Optional[Dict[str, Any]]:
        """Get section information by tag
        
        Args:
            tag: Section tag
            
        Returns:
            Section information dictionary or None if not found
        """
        return self.sections.get(tag)
    
    def get_sections_by_type(self, sec_type: str) -> List[Dict[str, Any]]:
        """Get all sections of a specific type
        
        Args:
            sec_type: Section type (e.g., 'Elastic', 'Fiber', etc.)
            
        Returns:
            List of section information dictionaries
        """
        result = []
        for section_info in self.sections.values():
            if section_info.get("type") == sec_type:
                result.append(section_info)
        return result
    
    def get_section_tags(self) -> List[int]:
        """Get all section tags
        
        Returns:
            List of section tags
        """
        return list(self.sections.keys())
    
    def clear(self):
        """Clear all section data"""
        self.sections.clear()

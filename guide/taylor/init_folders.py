import os

names = "VPC HH SB SS FT SC SR SX HP FD UD ICG HO CH HF CP FP M".split()

# full names
"""Virtual Pumpkin Carving
Hattori Hanzo’s Candy Shop
Spooky Briefcases
Scary Skeletons
Finding Treasure
Snatching Candy
Sammy Runes
Stacking Xorkins
Halloween Positioning
Frankenstein Dropout
Upstream Deliveries
Infinite Candy Glitch
House Ordering
Candy Hype
Heat Flow
Candy Packing
The Final Plan
Mystery

"""

d = {
    "VPC": "Virtual Pumpkin Carving",
    "HH": "Hattori Hanzo’s Candy Shop",
    "SB": "Spooky Briefcases",
    "SS": "Scary Skeletons",
    "FT": "Finding Treasure",
    "SC": "Snatching Candy",
    "SR": "Sammy Runes",
    "SX": "Stacking Xorkins",
    "HP": "Halloween Positioning",
    "FD": "Frankenstein Dropout",
    "UD": "Upstream Deliveries",
    "ICG": "Infinite Candy Glitch",
    "HO": "House Ordering",
    "CH": "Candy Hype",
    "HF": "Heat Flow",
    "CP": "Candy Packing",
    "FP": "The Final Plan",
    "M": "Mystery"
}

base_dir = os.path.dirname(os.path.abspath(__file__))

for name in names:
    folder_path = os.path.join(base_dir, name)
    os.makedirs(folder_path, exist_ok=True)

    for ext in ["py", "java", "cpp"]:
        file_path = os.path.join(folder_path, f"{name}.{ext}")
        if ext == "java":
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"// {d[name]} in Java\n")
                f.write(f"public class {name} {{\n")
                f.write(f"    public static void main(String[] args) {{\n")
                f.write(f"        // Your code here\n")
                f.write(f"    }}\n")
                f.write(f"}}\n")
        elif ext == "cpp":
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"// {d[name]} in C++\n")
                f.write(f"#include <iostream>\n\n")
                f.write(f"int main() {{\n")
                f.write(f"    // Your code here\n")
                f.write(f"    return 0;\n")
                f.write(f"}}\n")
        elif ext == "py":
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"# {d[name]} in Python\n")
                f.write(f"# Your code here\n")

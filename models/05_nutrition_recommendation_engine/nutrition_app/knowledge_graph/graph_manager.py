import networkx as nx
import pandas as pd
import os
from typing import Dict, List, Any
from nutrition_app.config import settings

class FoodKnowledgeGraph:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.initialize_graph()
        
    def initialize_graph(self):
        # Check if food store exists
        if not os.path.exists(settings.FOOD_STORE_PATH):
            print("Food feature store not found. Knowledge graph empty. Run preprocessor first.")
            return
            
        df = pd.read_csv(settings.FOOD_STORE_PATH)
        
        for _, row in df.iterrows():
            food_name = row['FoodName']
            food_id = int(row['FoodID'])
            
            # 1. Add Food Node
            self.graph.add_node(
                food_name, 
                type="Food",
                food_id=food_id,
                calories=float(row['Calories']),
                protein=float(row['Protein']),
                carbs=float(row['Carbohydrates']),
                fat=float(row['Fat']),
                fiber=float(row['Fiber']),
                glycemic_index=float(row['GlycemicIndex']),
                pcos_friendliness=float(row['pcos_friendliness_score'])
            )
            
            # 2. Category Connection
            category = str(row['Category'])
            self.graph.add_node(category, type="Category")
            self.graph.add_edge(food_name, category, relation="BELONGS_TO_CATEGORY")
            
            # 3. Glycemic Index Node
            gi = float(row['GlycemicIndex'])
            if gi <= 55:
                gi_class = "Low-GI"
            elif gi <= 69:
                gi_class = "Medium-GI"
            else:
                gi_class = "High-GI"
            self.graph.add_node(gi_class, type="GlycemicClass")
            self.graph.add_edge(food_name, gi_class, relation="HAS_GLYCEMIC_CLASS")
            
            # 4. Nutrient Richness Connections (Micro/Macronutrients)
            # Add nodes for Richness Types
            richness_markers = [
                ('Fiber', 3.0, 'High-Fiber'),
                ('Potassium_mg', 250.0, 'Potassium-Rich'),
                ('Magnesium_mg', 100.0, 'Magnesium-Rich'),
                ('Calcium_mg', 150.0, 'Calcium-Rich'),
                ('VitaminD_mcg', 1.0, 'VitaminD-Rich'),
                ('Zinc_mg', 2.0, 'Zinc-Rich'),
                ('Omega3_g', 0.5, 'Omega3-Rich'),
            ]
            for col, threshold, node_name in richness_markers:
                val = float(row.get(col, 0.0))
                if val >= threshold:
                    self.graph.add_node(node_name, type="NutrientRichness")
                    self.graph.add_edge(food_name, node_name, relation="RICH_IN")
                    
            # 5. Suitability Connections
            suitability_markers = [
                ('pcos_friendliness_score', 70.0, 'PCOS-Friendly', 'IS_SUITABLE_FOR'),
                ('InsulinResistanceSuitability', 70.0, 'Diabetes-Friendly', 'IS_SUITABLE_FOR'),
                ('HeartHealthIndicator', 70.0, 'Hypertension-Friendly', 'IS_SUITABLE_FOR'),
                ('WeightManagementScore', 70.0, 'Weight-Loss-Friendly', 'IS_SUITABLE_FOR'),
                ('HormonalHealthScore', 70.0, 'Hormone-Balancing', 'HAS_PROPERTY'),
                ('AntiInflammatoryPotential', 70.0, 'Anti-Inflammatory', 'HAS_PROPERTY')
            ]
            for score_col, threshold, node_name, relation in suitability_markers:
                score_val = float(row.get(score_col, 0.0))
                if score_val >= threshold:
                    self.graph.add_node(node_name, type="ConditionSuitability")
                    self.graph.add_edge(food_name, node_name, relation=relation)
                    
        print(f"Knowledge Graph populated with {self.graph.number_of_nodes()} nodes and {self.graph.number_of_edges()} edges.")
        
    def get_food_context(self, food_name: str) -> Dict[str, Any]:
        """
        Query graph to find all connections of a food.
        """
        matched_node = None
        for node in self.graph.nodes:
            if node.lower().strip() == food_name.lower().strip():
                matched_node = node
                break
                
        if matched_node is None:
            return {"food_name": food_name, "error": f"Food node '{food_name}' not found in Knowledge Graph."}
            
        node_data = self.graph.nodes[matched_node]
        
        # Find all outgoing edges
        connections = []
        for target in self.graph.successors(matched_node):
            edge_data = self.graph.get_edge_data(matched_node, target)
            target_data = self.graph.nodes[target]
            connections.append({
                "target": target,
                "type": target_data.get("type", "Unknown"),
                "relation": edge_data.get("relation", "Unknown")
            })
            
        return {
            "food_name": matched_node,
            "attributes": node_data,
            "semantic_connections": connections
        }
        
    def query_by_relation(self, target_node: str, relation: str) -> List[str]:
        """
        Find all foods connected to a target node with a specific relation.
        E.g. query_by_relation("PCOS-Friendly", "IS_SUITABLE_FOR")
        """
        matching_foods = []
        if not self.graph.has_node(target_node):
            return []
            
        # Traverse graph in reverse to find foods pointing to this target node
        for source in self.graph.predecessors(target_node):
            edge_data = self.graph.get_edge_data(source, target_node)
            if edge_data.get("relation") == relation:
                matching_foods.append(source)
                
        return matching_foods

# Singleton instance
graph_manager = None

def get_graph_manager() -> FoodKnowledgeGraph:
    global graph_manager
    if graph_manager is None:
        graph_manager = FoodKnowledgeGraph()
    return graph_manager

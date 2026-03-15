import os
import json
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from prompts import prompt_institution

def example_llm_policy_decision(model_historical_output:str, policy_historical:str) -> str:
    """
    Note:
       Gemini 3 can simultaneously use thinking mode and structured output.
    
    In this example, we expect the following output structure:
        {
            "reasoning": "reasoning process here.",
            "policy_decisions":{
                "agroforestry subsidy": 1,
                "agricultural landscape heterogeneity subsidy": 2,
                "intensive cropland tax": 3,
                "pasture tax": -1,
                "fodder tax": 3,
                "food crop subsidy": -2
            }
        }
    """

    # Load environment variables from .env file
    load_dotenv()
    
    # Make sure you have GEMINI_API_KEY set in your environment variables.
    # Alternatively, you can initialize the client with: client = genai.Client(api_key="YOUR_KEY")
    if not os.environ.get("GEMINI_API_KEY"):
        print("Warning: GEMINI_API_KEY environment variable is not set.")
        print("Please set it using: set GEMINI_API_KEY=your_key")
        print("Proceeding anyway to show client initialization, but API calls will fail.\n")
    
    # Initialize the official Google GenAI SDK client. This is mandatory.
    client = genai.Client()
    
    # First, we should update the prompt with the dynamic information from the simulation.
    # This is why we use formatted strings to define the prompts and use .format() to update the prompt with the dynamic information.
    # Let's assume the following historical land use and ecosystem services supply and policy decisions:
    prompt_institution_updated = prompt_institution.format(
        model_historical_output = model_historical_output,
        policy_historical = policy_historical   
    )

    # Second, we should define the output schema for the policy decisions.
    # Because the expected output is a nested dictionary, we need to define a Pydantic schema for the policy decisions.
    # The alias parameter is used to map the field name in the Pydantic schema to the field name in the expected output.
    class PolicyDecisions(BaseModel):
        agroforestry_subsidy: int = Field(alias="agroforestry subsidy")
        agricultural_landscape_heterogeneity_subsidy: int = Field(alias="agricultural landscape heterogeneity subsidy")
        intensive_cropland_tax: int = Field(alias="intensive cropland tax")
        pasture_tax: int = Field(alias="pasture tax")
        fodder_tax: int = Field(alias="fodder tax")
        food_crop_subsidy: int = Field(alias="food crop subsidy")

    # Third, we should define a Pydantic schema for the overall output
    class OutputSchema(BaseModel):
        reasoning: str = Field(description="The reasoning process of how you came up with the policy decisions.")
        policy_decisions: PolicyDecisions = Field(description="The policy decisions.")

    # Fourth, we should configure the model to use thinking mode and structured output.
    # Note: This is the core function that takes the prompt and the configuration as input and returns the response.
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt_institution_updated,
        config=types.GenerateContentConfig(
            # Higher temperature for more creativity; lower for more deterministic output. (Valid range: 0.0 to 2.0)
            temperature=0.0,
            # Enable Thinking Mode
            thinking_config=types.ThinkingConfig(
                include_thoughts=True,
                # Define the thinking level
                thinking_level="MEDIUM"  # Options: LOW, MEDIUM, HIGH (Deep Think)
            ),
            # Enable Structured Output
            response_mime_type="application/json",
            response_schema=OutputSchema,
        )
    )

    return response


def main():

    # The following information should come from your simulation model.
    model_historical_output="""
        {
            "agroforestry area": [0.01, 0.01, 0.011],
            "agricultural landscape heterogeneity": [0.05, 0.06, 0.06],
            "climate-friendly agricultural area": [0.15, 0.14, 0.13],
            "food crop supply": [0.2, 0.21, 0.22]
        }
        """
    policy_historical="""
        {
            "agroforestry subsidy": 0,
            "agricultural landscape heterogeneity subsidy": 0,
            "intensive cropland tax": 0,
            "pasture tax": 0,
            "fodder tax": 0,
            "food crop subsidy": 0
        }
        """

    try:
        response = example_llm_policy_decision(model_historical_output, policy_historical)
    except Exception as e:
        print(f"\nAPI Error / Exception: {e}")

    # Extracting the separate components
    print("--- THE MODEL'S REASONING ---")
    for part in response.candidates[0].content.parts:
        if part.thought:
            print(part.text)

    print("\n--- THE STRUCTURED JSON OUTPUT ---")
    # The final part (non-thought) will contain the valid JSON
    final_json_text = response.text 
    parsed_json = json.loads(final_json_text)
    print(json.dumps(parsed_json, indent=2))
    


if __name__ == "__main__":
    main()


"""
Expected output:

--- THE MODEL'S REASONING ---
**My Assessment and Strategic Intervention**

Okay, here's the situation as I see it, based on the data. We're looking at four key agricultural targets, and I need to formulate a plan that is effective but also keeps the budget constraint in mind.  It appears we're facing challenges across multiple metrics. Specifically, agroforestry coverage is practically non-existent, high-diversity landscapes are stagnant below our target, climate-friendly practices are declining, and while food crop production is increasing, we need to ensure this continues.

My initial assessment reveals a need for action on several fronts. *Agroforestry* is almost negligible, so a substantial boost through a subsidy increase is imperative. *Agricultural landscape heterogeneity* is also underperforming. To achieve the 10% target, a solid subsidy is required. The decreasing trend in *climate-friendly agricultural practices* is alarming, so I need to disincentivize intensive practices that are contributing to this decline. And although *food crop supply* is currently 
increasing, to further secure this trajectory, I must implement a subsidy. Furthermore, extensive livestock-based land use should be discouraged.

I've examined several policy instruments. Subsidies for agroforestry and agricultural landscape heterogeneity are essential to stimulate growth in those sectors. Taxes on intensive cropland are my most important tool for addressing the decline in climate-friendly practices. A tax on pasture land and fodder will help discourage less diverse uses. To support and encourage the production of nutritious crops, I will boost this area with a subsidy.

I recognize a "minor budget constraint." This means I cannot tax to increase the budget and so, need to be fiscally responsible with my subsidy increases. I also must address the tax.

After careful consideration of the data and potential policy instruments, I've arrived at my final strategy:

*   I must boost the *agroforestry subsidy* significantly, to level 3, because it's at a very low level.
*   The *agricultural landscape heterogeneity subsidy* needs an aggressive push to reach 10%, I will apply level 2.
*   I'll apply an intensive cropland tax at level 2.
*   A moderate *fodder tax* at level 1 to further discourage less diverse land use.
*   And finally, a food crop subsidy to reinforce this positive trend with a level 2 increase.
*   I will also apply a moderate pasture tax at level 1 to discourage less diverse land use.

With these policies in place, the goal is to shift agricultural practices toward more sustainable and diversified models while ensuring food security. The plan is well-reasoned and balanced, considering the budget constraints and the need to address 
specific target areas.


--- THE STRUCTURED JSON OUTPUT ---
{
  "reasoning": "Historical trends show a decline in climate-friendly agricultural areas (from 0.15 to 0.13) and stagnation in agroforestry (0.011) and landscape heterogeneity (0.06). To reach the 10% heterogeneity target and expand agroforestry, I am increasing their respective subsidies by Level 2 and Level 3. To reverse the decline in climate-friendly practices, I am increasing the intensive cropland tax (Level 2) and fodder tax (Level 1). To ensure continued growth in nutritious food crop supply, I am increasing the food crop subsidy by Level 2. A Level 1 tax on pasture land is also implemented to encourage land-use diversification and shift towards more sustainable practices.",
  "policy_decisions": {
    "agroforestry subsidy": 3,
    "agricultural landscape heterogeneity subsidy": 2,
    "intensive cropland tax": 2,
    "pasture tax": 1,
    "fodder tax": 1,
    "food crop subsidy": 2
  }
}

"""
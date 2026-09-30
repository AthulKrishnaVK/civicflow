# from langgraph.graph import StateGraph, START, END

# from app.models.schemas import AgentState
# from app.agents.verification import verify_claims
# from app.agents.supervisor import analyze_goal
# from app.agents.eligibility import analyze_eligibility
# from app.agents.research import research_agent
# from app.agents.documents import analyze_documents
# from app.agents.regulations import analyze_regulations
# from app.agents.procedure import analyze_procedure


# def supervisor_node(state: AgentState):

#     intent = analyze_goal(
#         state["user_input"]
#     )

#     return {
#         "intent": intent.model_dump()
#     }


# def eligibility_node(state: AgentState):

#     eligibility = analyze_eligibility(
#         state["intent"]
#     )

#     return {
#         "eligibility": eligibility.model_dump()
#     }


# def research_node(state: AgentState):

#     return research_agent(state)

# def verification_node(state: AgentState):

#     verification = verify_claims(state)

#     return {
#         "verification": verification.model_dump()
#     }
# def documents_node(state: AgentState):

#     documents = analyze_documents(state)

#     return {
#         "documents": documents.model_dump()
#     }


# def regulations_node(state: AgentState):

#     regulations = analyze_regulations(state)

#     return {
#         "regulations": regulations.model_dump()
#     }


# def procedure_node(state: AgentState):

#     procedure = analyze_procedure(state)

#     return {
#         "procedure": procedure.model_dump()
#     }


# def build_graph():

#     graph = StateGraph(AgentState)

#     graph.add_node(
#         "supervisor",
#         supervisor_node
#     )

#     graph.add_node(
#         "eligibility",
#         eligibility_node
#     )

#     graph.add_node(
#         "research",
#         research_node
#     )
#     graph.add_node(
#     "verification",
#     verification_node
# )

#     graph.add_node(
#         "documents",
#         documents_node
#     )

#     graph.add_node(
#         "regulations",
#         regulations_node
#     )

#     graph.add_node(
#         "procedure",
#         procedure_node
#     )

#     graph.add_edge(
#         START,
#         "supervisor"
#     )

#     graph.add_edge(
#         "supervisor",
#         "eligibility"
#     )

#     graph.add_edge(
#         "eligibility",
#         "research"
#     )

#     graph.add_edge(
#         "research",
#         "documents"
#     )

#     graph.add_edge(
#         "documents",
#         "regulations"
#     )

#     graph.add_edge(
#         "regulations",
#         "procedure"
#     )

#     graph.add_edge(
#         "procedure",
#         "verification"
#     )
#     graph.add_edge(
#     "verification",
#     END
# )

#     return graph.compile()


# civicflow_graph = build_graph()

from langgraph.graph import StateGraph, START, END

from app.models.schemas import AgentState

from app.agents.supervisor import analyze_goal
from app.agents.source_discovery import analyze_sources
from app.agents.research import research_agent
from app.agents.eligibility import analyze_eligibility
from app.agents.documents import analyze_documents
from app.agents.regulations import analyze_regulations
from app.agents.procedure import analyze_procedure
from app.agents.verification import verify_claims


def supervisor_node(state: AgentState):

    intent = analyze_goal(
        state["user_input"]
    )

    return {
        "intent": intent.model_dump()
    }


def source_discovery_node(state: AgentState):

    result = analyze_sources(
        state["user_input"],
        state["intent"]
    )

    return {
        "sources": [
            source.model_dump()
            for source in result.sources
        ]
    }


def research_node(state: AgentState):

    return research_agent(state)


def eligibility_node(state: AgentState):

    eligibility = analyze_eligibility(
        state
    )

    return {
        "eligibility": eligibility.model_dump()
    }


def documents_node(state: AgentState):

    documents = analyze_documents(
        state
    )

    return {
        "documents": documents.model_dump()
    }


def regulations_node(state: AgentState):

    regulations = analyze_regulations(
        state
    )

    return {
        "regulations": regulations.model_dump()
    }


def procedure_node(state: AgentState):

    procedure = analyze_procedure(
        state
    )

    return {
        "procedure": procedure.model_dump()
    }


def verification_node(state: AgentState):

    verification = verify_claims(
        state
    )

    return {
        "verification": verification.model_dump()
    }


def build_graph():

    graph = StateGraph(
        AgentState
    )

    graph.add_node(
        "supervisor",
        supervisor_node
    )

    graph.add_node(
        "source_discovery",
        source_discovery_node
    )

    graph.add_node(
        "research",
        research_node
    )

    graph.add_node(
        "eligibility",
        eligibility_node
    )

    graph.add_node(
        "documents",
        documents_node
    )

    graph.add_node(
        "regulations",
        regulations_node
    )

    graph.add_node(
        "procedure",
        procedure_node
    )

    graph.add_node(
        "verification",
        verification_node
    )

    graph.add_edge(
        START,
        "supervisor"
    )

    graph.add_edge(
        "supervisor",
        "source_discovery"
    )

    graph.add_edge(
        "source_discovery",
        "research"
    )

    graph.add_edge(
        "research",
        "eligibility"
    )

    graph.add_edge(
        "eligibility",
        "documents"
    )

    graph.add_edge(
        "documents",
        "regulations"
    )

    graph.add_edge(
        "regulations",
        "procedure"
    )

    graph.add_edge(
        "procedure",
        "verification"
    )

    graph.add_edge(
        "verification",
        END
    )

    return graph.compile()


civicflow_graph = build_graph()
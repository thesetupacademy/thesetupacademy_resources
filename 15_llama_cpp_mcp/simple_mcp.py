from mcp.server.mcpserver import MCPServer

#Init
mcp = MCPServer("the_setup_academy_mcp_server")

#Tool
@mcp.tool()
def add_numbers(a: int, b: int):
    """Add 2 Integer Numbers"""
    print("MCP tool: add_numbers called")
    return a+b

#Tool 2
@mcp.tool()
def subtract_numbers(a: int, b: int):
    """Subtract 2 Integer Numbers"""
    print("MCP tool: subtract_numbers called")
    return a-b

def start_mcp():
    print("MCP server started")
    mcp.run()

#call main
if __name__ == "__main__":
    start_mcp()
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using TutorinoAPICS.Models;

namespace TutorinoAPICS.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class AvailableController : ControllerBase
    {
        public readonly IConfiguration configuration;
        public AvailableController(IConfiguration configuration)
        {
            this.configuration = configuration;
        }
    }
}

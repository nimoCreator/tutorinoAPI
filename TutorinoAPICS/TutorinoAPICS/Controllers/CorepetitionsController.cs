using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using TutorinoAPICS.Models;
using Newtonsoft.Json;
using System.Data;
using System.Data.SqlClient;

namespace TutorinoAPICS.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class CorepetitionsController : ControllerBase
    {
        public readonly IConfiguration configuration;
        public CorepetitionsController(IConfiguration configuration)
        {
            this.configuration = configuration;
        }

    }

    

}

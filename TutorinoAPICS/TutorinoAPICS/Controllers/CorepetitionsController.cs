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

        [HttpGet]
        [Route("getTrans")]
        public String getTrans()
        {
            SqlConnection con = new SqlConnection(configuration.GetConnectionString("AppCon").ToString());
            SqlDataAdapter data = new SqlDataAdapter("Select * from corepetitions", con);
            DataTable dataTable = new DataTable();
            data.Fill(dataTable);
            List<Corepetitions> list = new List<Corepetitions>();
            if (dataTable.Rows.Count > 0)
            {
                for (int i = 0; i < dataTable.Rows.Count; i++)
                {
                    Corepetitions core = new Corepetitions();
                    core.zuid = Convert.ToInt32(dataTable.Rows[i]["zuid"]);
                    core.teacher = Convert.ToInt32(dataTable.Rows[i]["teacher"]);
                    core.pupil = Convert.ToInt32(dataTable.Rows[i]["pupil"]);
                    core.subject = Convert.ToInt32(dataTable.Rows[i]["subject"]);
                    core.level = Convert.ToInt32(dataTable.Rows[i]["level"]);
                    core.status = Convert.ToString(dataTable.Rows[i]["status"]);
                    core.start = Convert.ToDateTime(dataTable.Rows[i]["start"]);
                    core.end = Convert.ToDateTime(dataTable.Rows[i]["end"]);
                    core.time = Convert.ToInt32(dataTable.Rows[i]["time"]);
                    core.price = Convert.ToDouble(dataTable.Rows[i]["price"]);
                    core.currency = Convert.ToString(dataTable.Rows[i]["currency"]);
                    core.form = Convert.ToChar(dataTable.Rows[i]["form"]);
                    core.meet_link = Convert.ToString(dataTable.Rows[i]["meet_link"]);
                    core.table_link = Convert.ToString(dataTable.Rows[i]["table_link"]);
                    core.localization = Convert.ToString(dataTable.Rows[i]["localization"]);
                    core.accepted_o = Convert.ToBoolean(dataTable.Rows[i]["accepted_o"]);
                    core.accepted_k = Convert.ToBoolean(dataTable.Rows[i]["accepted_k"]);
                    core.paid_in_cash = Convert.ToBoolean(dataTable.Rows[i]["paid_in_cash"]);
                    core.trainsaction_id = Convert.ToInt32(dataTable.Rows[i]["trainsaction_id"]);
                    core.convo = Convert.ToInt32(dataTable.Rows[i]["convo"]);
                    list.Add(core);
                }
            }
            if (list.Count > 0)
            {
                return JsonConvert.SerializeObject(list);
            }
            else
            {
                return JsonConvert.SerializeObject(new Response());
            }
        }
    }
}

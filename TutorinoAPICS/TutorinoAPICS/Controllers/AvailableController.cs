using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json;
using System.Data;
using System.Data.SqlClient;
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

    [HttpPost]
    [Route("AddAvailable")]
    public String addAval(Available aval){
        SqlConnection con = new SqlConnection(configuration.GetConnectionString("AppCon").ToString());
        SqlCommand cmd = new SqlCommand("Insert into available(user_uuid,weekday,\"begin\",end,valid_from,valid_until) values('" + aval.user_uuid + "','" + aval.weekday + "','" + aval.begin + "','" + aval.end + "','" + aval.valid_from + "','" + aval.valid_until + "')", con);
        con.Open();
        int i;
        try
        {
            i = cmd.ExecuteNonQuery();
        } catch (Exception ex)
        {
            return JsonConvert.SerializeObject(new Response(102, ex.ToString()));
        }
        con.Close();
        if (i > 0)
        {
            return JsonConvert.SerializeObject(new Response(0, "Available added"));
        }
        else
        {
            return JsonConvert.SerializeObject(new Response());
        }
    }

    [HttpPost]
    [Route("editAval")]
    public String editAval(AvailableChange aval){
        SqlConnection con = new SqlConnection(configuration.GetConnectionString("AppCon").ToString());
        SqlCommand cmd = new SqlCommand("Update available Set user_uuid=" + aval.user_uuid +" Where uuid=" + aval.aid, con);
        con.Open();
        int i;
        try
        {
            i = cmd.ExecuteNonQuery();
        } catch (Exception ex)
        {
            return JsonConvert.SerializeObject(new Response(102, "Internal Error"));
        }
        con.Close();
        if (i > 0)
        {
            return JsonConvert.SerializeObject(new Response(0, "Data Edited"));
        }
        else
        {
            return JsonConvert.SerializeObject(new Response());
        }
    }

        [HttpPost]
        [Route("getAval")]
        public String getAval(AvalID aval)
        {
            SqlConnection con = new SqlConnection(configuration.GetConnectionString("AppCon").ToString());
            SqlDataAdapter data = new SqlDataAdapter("Select * from available where user_uuid=" + aval.user_uuid, con);
            DataTable dataTable = new DataTable();
            data.Fill(dataTable);
            List<Available> a = new List<Available>();
            if (dataTable.Rows.Count > 0)
            {
                for (int i = 0; i < dataTable.Rows.Count; i++)
                {
                    Available newA = new Available();
                    newA.weekday = Convert.ToInt32(dataTable.Rows[i]["weekday"]);
                    newA.begin = Convert.ToInt32(dataTable.Rows[i]["begin"]);
                    newA.end = Convert.ToInt32(dataTable.Rows[i]["end"]);
                    newA.valid_from = Convert.ToDateTime(dataTable.Rows[i]["valid_from"]);
                    newA.valid_until = Convert.ToDateTime(dataTable.Rows[i]["valid_until"]);
                    a.Add(newA);
                }
            }
            if (a.Count > 0)
            {
                return JsonConvert.SerializeObject(a);
            }
            else
            {
                return JsonConvert.SerializeObject(new Response(100, "No data available"));
            }
        }
    }
}

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
    public class TransactionsController : ControllerBase
    {
        public readonly IConfiguration configuration;
        public CorepetitionsController(IConfiguration configuration)
        {
            this.configuration = configuration;
        }

        [HttpPost]
        [Route("newTransaction")]
        public String newTrans(Transaction trans){
            SqlConnection con = new SqlConnection(configuration.GetConnectionString("AppCon").ToString());
            SqlCommand cmd = new SqlCommand("Insert into transactions(statu,ouid,trans_date,value,currency,details) values(@status,@ouid,@trans_date,@value,@currency,@details)", con);
            cmd.Parameters.Add("@trans_date", SqlDbType.DateTime).Value = trans.trans_date;
            cmd.Parameters.Add("@status", SqlDbType.VarChar).Value = trans.status;
            cmd.Parameters.Add("@ouid", SqlDbType.Int).Value = trans.ouid;
            cmd.Parameters.Add("@birthdate", SqlDbType.DateTime).Value = 
            cmd.Parameters.Add("@pfp", SqlDbType.VarChar).Value = 
            con.Open();
            int i;
            try
            {
                i = cmd.ExecuteNonQuery();
            } catch (Exception ex)
            {
                return JsonConvert.SerializeObject(new Response(102, "User Exists"));
            }
            con.Close();
            if (i > 0)
            {
                return JsonConvert.SerializeObject(new Response(0, "Data added"));
            }
            else
            {
                return JsonConvert.SerializeObject(new Response());
            }
        }
    }
}

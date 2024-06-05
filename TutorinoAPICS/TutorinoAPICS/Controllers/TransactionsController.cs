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
        public TransactionsController(IConfiguration configuration)
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
            cmd.Parameters.Add("@value", SqlDbType.Float).Value = trans.value; 
            cmd.Parameters.Add("@currency", SqlDbType.VarChar).Value = trans.currency;
            cmd.Parameters.Add("@details", SqlDbType.VarChar).Value = trans.details;
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
                return JsonConvert.SerializeObject(new Response(0, "Transaction added"));
            }
            else
            {
                return JsonConvert.SerializeObject(new Response());
            }
        }

        [HttpPost]
        [Route("updateTrans")]
        public String updateTrans(EditTrans trans){
            SqlConnection con = new SqlConnection(configuration.GetConnectionString("AppCon").ToString());
            SqlCommand cmd = new SqlCommand("Update transactions Set trans_confirmed=@conf_date,status=@status Where tid=@tid", con);
            cmd.Parameters.Add("@conf_date", SqlDbType.DateTime).Value = trans.conf_date;
            cmd.Parameters.Add("@status", SqlDbType.VarChar).Value = trans.status;
            cmd.Parameters.Add("@tid", SqlDbType.Int).Value = trans.tid;
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
        [Route("getTrans")]
        public String getTrans(ListTrans trans){
            SqlConnection con = new SqlConnection(configuration.GetConnectionString("AppCon").ToString());
            SqlDataAdapter data = new SqlDataAdapter("Select * from transactions WHERE ouid="+trans.ouid, con);
            DataTable dataTable = new DataTable();
            data.Fill(dataTable);
            List<PrintTrans> tran = new List<PrintTrans>();
            if (dataTable.Rows.Count > 0)
            {
                for (int i = 0; i < dataTable.Rows.Count; i++)
                {
                    PrintTrans t = new PrintTrans();
                    t.tid = Convert.ToInt32(dataTable.Rows[i]["tid"]);
                    t.status = Convert.ToString(dataTable.Rows[i]["statu"]);
                    t.conf_date = Convert.ToDateTime(dataTable.Rows[i]["trans_date"]);
                    t.trans_date = Convert.ToDateTime(dataTable.Rows[i]["trans_confirmed"]);
                    t.value = Convert.ToDouble(dataTable.Rows[i]["value"]);
                    t.currency = Convert.ToString(dataTable.Rows[i]["currency"]);
                    t.status = Convert.ToString(dataTable.Rows[i]["details"]);
                    tran.Add(t);
                }
            }
            if(tran.Count>0)
            {
                return JsonConvert.SerializeObject(tran);
            }
            else
            {
                return JsonConvert.SerializeObject(new Response());
            }
        }

        [HttpPost]
        [Route("getLastTrans")]
        public String getLastTrans(ListTrans trans){
            SqlConnection con = new SqlConnection(configuration.GetConnectionString("AppCon").ToString());
            SqlDataAdapter data = new SqlDataAdapter("SELECT TOP 1 * FROM transactions WHERE ouid =" + trans.ouid +" ORDER BY tid DESC", con);
            PrintTrans t = new PrintTrans();
            DataTable dataTable = new DataTable();
            data.Fill(dataTable);
            if (dataTable.Rows.Count > 0)
            {
                t.tid = Convert.ToInt32(dataTable.Rows[0]["tid"]);
                t.status = Convert.ToString(dataTable.Rows[0]["statu"]);
                t.conf_date = Convert.ToDateTime(dataTable.Rows[0]["trans_date"]);
                t.trans_date = Convert.ToDateTime(dataTable.Rows[0]["trans_confirmed"]);
                t.value = Convert.ToDouble(dataTable.Rows[0]["value"]);
                t.currency = Convert.ToString(dataTable.Rows[0]["currency"]);
                t.status = Convert.ToString(dataTable.Rows[0]["details"]);
                return JsonConvert.SerializeObject(t);
            }
            else
            {
                return JsonConvert.SerializeObject(new Response(100,"No Transactions for this offer"));
            }
        }

        [HttpPost]
        [Route("DeleteTransaction")]
        public String deleteTransaction(DeleteTrans tran){
            SqlConnection con = new SqlConnection(configuration.GetConnectionString("AppCon").ToString());
            SqlCommand cmd = new SqlCommand("Delete from transactions Where tid=@uuid", con);
            cmd.Parameters.Add("@uuid", SqlDbType.Int).Value = tran.tid;
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
                return JsonConvert.SerializeObject(new Response(0, "Transaction Deleted"));
            }
            else
            {
                return JsonConvert.SerializeObject(new Response());
            }
        }
    }
}

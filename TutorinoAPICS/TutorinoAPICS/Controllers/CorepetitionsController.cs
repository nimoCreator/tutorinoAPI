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
        [Route("getAllComps")]
        public String getAllCorepetitions()
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
                    core.trainsaction_id = Convert.ToInt32(dataTable.Rows[i]["transaction_id"]);
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

        [HttpGet]
        [Route("getCorepetition")]
        public String getCorepetition(GetCorepet corp)
        {
            SqlConnection con = new SqlConnection(configuration.GetConnectionString("AppCon").ToString());
            SqlDataAdapter data = new SqlDataAdapter("Select * from corepetitions where zuid=" + corp.zuid, con);
            DataTable dataTable = new DataTable();
            data.Fill(dataTable);
            if (dataTable.Rows.Count > 0)
            {
                    Corepetitions core = new Corepetitions();
                    core.zuid = Convert.ToInt32(dataTable.Rows[0]["zuid"]);
                    core.teacher = Convert.ToInt32(dataTable.Rows[0]["teacher"]);
                    core.pupil = Convert.ToInt32(dataTable.Rows[0]["pupil"]);
                    core.subject = Convert.ToInt32(dataTable.Rows[0]["subject"]);
                    core.level = Convert.ToInt32(dataTable.Rows[0]["level"]);
                    core.status = Convert.ToString(dataTable.Rows[0]["status"]);
                    core.start = Convert.ToDateTime(dataTable.Rows[0]["start"]);
                    core.end = Convert.ToDateTime(dataTable.Rows[0]["end"]);
                    core.time = Convert.ToInt32(dataTable.Rows[0]["time"]);
                    core.price = Convert.ToDouble(dataTable.Rows[0]["price"]);
                    core.currency = Convert.ToString(dataTable.Rows[0]["currency"]);
                    core.form = Convert.ToChar(dataTable.Rows[0]["form"]);
                    core.meet_link = Convert.ToString(dataTable.Rows[0]["meet_link"]);
                    core.table_link = Convert.ToString(dataTable.Rows[0]["table_link"]);
                    core.localization = Convert.ToString(dataTable.Rows[0]["localization"]);
                    core.accepted_o = Convert.ToBoolean(dataTable.Rows[0]["accepted_o"]);
                    core.accepted_k = Convert.ToBoolean(dataTable.Rows[0]["accepted_k"]);
                    core.paid_in_cash = Convert.ToBoolean(dataTable.Rows[0]["paid_in_cash"]);
                    core.trainsaction_id = Convert.ToInt32(dataTable.Rows[0]["transaction_id"]);
                    core.convo = Convert.ToInt32(dataTable.Rows[0]["convo"]);
                    return JsonConvert.SerializeObject(core);
            }
            else
            {
                return JsonConvert.SerializeObject(new Response());
            }
        }

        [HttpPost]
        [Route("newCorepetition")]
        public String newTrans(NewCopepetition core){
            int choosenSubject;
            switch(core.subject){
                case "math":
                    choosenSubject = 0;
                    break;
                case "phys":
                    choosenSubject = 1;
                    break;
                case "chem":
                    choosenSubject = 2;
                    break;
                case "bio":
                    choosenSubject = 3;
                    break;
                case "hist":
                    choosenSubject = 4;
                    break;
                case "geo":
                    choosenSubject = 5;
                    break;
                case "eng":
                    choosenSubject = 6;
                    break;
                default:
                    choosenSubject = 7;
                    break;
            }
            SqlConnection con = new SqlConnection(configuration.GetConnectionString("AppCon").ToString());
            SqlCommand cmd = new SqlCommand("Insert into corepetitions(teacher,pupil,subject,level,status,start,end,time,price,currency,form,meet_link,table_link,localization,accepted_o,accepted_k,paid_in_cash,transaction_id) values(@1,@2,@3,@4,@5,@6,@7,@8,@9,@10,@11,@12,@13,@14,@15,@16,@17,@18,@19)", con);
            cmd.Parameters.Add("@1", SqlDbType.Int).Value =core.teacher;
            cmd.Parameters.Add("@2", SqlDbType.Int).Value = core.pupil;
            cmd.Parameters.Add("@3", SqlDbType.Int).Value =choosenSubject;
            cmd.Parameters.Add("@4", SqlDbType.Int).Value =core.level;
            cmd.Parameters.Add("@5", SqlDbType.VarChar).Value =core.status;
            cmd.Parameters.Add("@6", SqlDbType.DateTime).Value =core.start;
            cmd.Parameters.Add("@7", SqlDbType.DateTime).Value =core.end;
            cmd.Parameters.Add("@8", SqlDbType.Int).Value =core.time;
            cmd.Parameters.Add("@9", SqlDbType.Float).Value =core.price;
            cmd.Parameters.Add("@10", SqlDbType.VarChar).Value =core.currency;
            cmd.Parameters.Add("@11", SqlDbType.Char).Value =core.form;
            cmd.Parameters.Add("@12", SqlDbType.VarChar).Value =core.meet_link;
            cmd.Parameters.Add("@13", SqlDbType.VarChar).Value =core.table_link;
            cmd.Parameters.Add("@14", SqlDbType.VarChar).Value =core.localization;
            cmd.Parameters.Add("@15", SqlDbType.Bit).Value =core.accepted_o;
            cmd.Parameters.Add("@16", SqlDbType.Bit).Value =core.accepted_k;
            cmd.Parameters.Add("@17", SqlDbType.Bit).Value =core.paid_in_cash;
            cmd.Parameters.Add("@18", SqlDbType.Int).Value =core.trainsaction_id;
            cmd.Parameters.Add("@19", SqlDbType.Int).Value =core.convo;
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
                return JsonConvert.SerializeObject(new Response(0, "Corepetition added"));
            }
            else
            {
                return JsonConvert.SerializeObject(new Response());
            }
        }

        [HttpPost]
        [Route("editCorepetition")]
        public String editCorepetition(EditCopepetition core){
            int choosenSubject;
            switch(core.subject){
                case "math":
                    choosenSubject = 0;
                    break;
                case "phys":
                    choosenSubject = 1;
                    break;
                case "chem":
                    choosenSubject = 2;
                    break;
                case "bio":
                    choosenSubject = 3;
                    break;
                case "hist":
                    choosenSubject = 4;
                    break;
                case "geo":
                    choosenSubject = 5;
                    break;
                case "eng":
                    choosenSubject = 6;
                    break;
                default:
                    choosenSubject = 7;
                    break;
            }
            SqlConnection con = new SqlConnection(configuration.GetConnectionString("AppCon").ToString());
            SqlCommand cmd = new SqlCommand("Update corepetitions Set teacher=@1,pupil=@2,subject=@3,level=@4,status=@5,start=@6,end=@7,time=@8,price=@9,currency=@10,form=@11,meet_link=@12,table_link=@13,localization=@14,accepted_o=@15,accepted_k=@16,paid_in_cash=@17,transaction_id=@18,convo=@19 Where zuid=" + core.zuid, con);
            cmd.Parameters.Add("@1", SqlDbType.Int).Value =core.teacher;
            cmd.Parameters.Add("@2", SqlDbType.Int).Value = core.pupil;
            cmd.Parameters.Add("@3", SqlDbType.Int).Value =choosenSubject;
            cmd.Parameters.Add("@4", SqlDbType.Int).Value =core.level;
            cmd.Parameters.Add("@5", SqlDbType.VarChar).Value =core.status;
            cmd.Parameters.Add("@6", SqlDbType.DateTime).Value =core.start;
            cmd.Parameters.Add("@7", SqlDbType.DateTime).Value =core.end;
            cmd.Parameters.Add("@8", SqlDbType.Int).Value =core.time;
            cmd.Parameters.Add("@9", SqlDbType.Float).Value =core.price;
            cmd.Parameters.Add("@10", SqlDbType.VarChar).Value =core.currency;
            cmd.Parameters.Add("@11", SqlDbType.Char).Value =core.form;
            cmd.Parameters.Add("@12", SqlDbType.VarChar).Value =core.meet_link;
            cmd.Parameters.Add("@13", SqlDbType.VarChar).Value =core.table_link;
            cmd.Parameters.Add("@14", SqlDbType.VarChar).Value =core.localization;
            cmd.Parameters.Add("@15", SqlDbType.Bit).Value =core.accepted_o;
            cmd.Parameters.Add("@16", SqlDbType.Bit).Value =core.accepted_k;
            cmd.Parameters.Add("@17", SqlDbType.Bit).Value =core.paid_in_cash;
            cmd.Parameters.Add("@18", SqlDbType.Int).Value =core.trainsaction_id;
            cmd.Parameters.Add("@19", SqlDbType.Int).Value =core.convo;
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
                return JsonConvert.SerializeObject(new Response(0, "Corepetition edited"));
            }
            else
            {
                return JsonConvert.SerializeObject(new Response());
            }
        }

        [HttpPost]
        [Route("DeleteCorepetiton")]
        public String deleteCorepetion(GetCorepet core){
            SqlConnection con = new SqlConnection(configuration.GetConnectionString("AppCon").ToString());
            SqlCommand cmd = new SqlCommand("Delete from corepetitions Where zuid=@uuid", con);
            cmd.Parameters.Add("@uuid", SqlDbType.Int).Value = core.zuid;
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
                return JsonConvert.SerializeObject(new Response(0, "Corepetition Deleted"));
            }
            else
            {
                return JsonConvert.SerializeObject(new Response());
            }
        }
    }
}

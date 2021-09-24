using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using ${projectName}.Service.Models.Interface;
using Newtonsoft.Json;

namespace ${projectName}.Models
{

    public class AbstractEntity : IEntity
    {

        [Key]
        [Column("id")]
        public long Id { get; set; }

        [Column("scope_id")]
        [JsonIgnore]
        public long? ScopeId { get; set; }

        [JsonIgnore]
        public Scope Scope { get; set; }


        /* Informações de auditoria*/

        [Column("created_on")]
        // [JsonIgnore]
        public DateTime? CreatedOn { get; set; }

        [Column("updated_on")]
        // [JsonIgnore]
        public DateTime? UpdatedOn { get; set; }

        [Column("created_by")]
        [JsonIgnore]
        public int? CreatedBy { get; set; }

        [Column("updated_by")]
        [JsonIgnore]
        public int? UpdatedBy { get; set; }
    }

}
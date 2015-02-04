'''
Class to hold the options for ample
'''
# python imports
import os

# our imports
import version

class AmpleOptions(object):

    def __init__(self):
        # The dictionary with all the options
        self.d = {}

        # dictionary with the default arguments - if any are paths add to paths in populate
        self.defaults = {
                            'alignment_file' : None,
                            'all_atom' : True,
                            'arpwarp_cycles' : 10,
                            'ASU' : 0,
                            'benchmark_mode' : False,
                            'blast_dir' : None,
                            'buccaneer_cycles' : 5,
                            'cluster_method' : 'spicker',
                            'ccp4_jobid' : None,
                            'debug' : False,
                            'domain_all_chains_pdb' : None,
                            'domain_termini_distance' : 0,
                            'early_terminate' : True,
                            'ensemble_mode' : 'percent',
                            'ensembler' : False,
                            'ensembles_dir' : None,
                            'F' : None,
                            'fasta' : None,
                            'frags_3mers' : None,
                            'frags_9mers' : None,
                            'FREE' : None,
                            'import_models' : False,
                            'import_ensembles' : False,
                            'improve_template' : None,
                            'LGA' : None,
                            'make_frags' : False,
                            'make_models' : True,
                            'maxcluster_exe' : None,
                            'max_ensemble_models' : 30,
                            'missing_domain' : False,
                            'models_dir' : None,
                            'molrep_only' : False,
                            'mr_keys' : None,
                            'mr_sequence' : None,
                            'mtz' : None,
                            'name' : 'ampl',
                            'native_pdb' : None,
                            'nmodels' : 1000,
                            'NMR_model_in' : None,
                            'NMR_process' : None,
                            'NMR_protocol' : False,
                            'NMR_remodel_fasta' : None,
                            'NMR_Truncate_only' : None,
                            'nproc' : 1,
                            'nr' : None,
                            'num_clusters' : 1,
                            'old_shelx' : False,
                            'output_pdb' : 'ample_output.pdb',
                            'percent' : 5,
                            'phaser_only' : False,
                            'phaser_kill' : 0,
                            'phenix_exe' : None,
                            'psipred_ss2' : None,
                            'quark_models' : None,
                            'rg_reweight' : None,
                            'ROSETTA_cluster' : None,
                            'rosetta_db' : None,
                            'rosetta_dir' : None,
                            'rosetta_fragments_exe' : None,
                            'rosetta_AbinitioRelax' : None,
                            'rosetta_version' : None,
                            'rcdir' : os.path.join( os.path.expanduser("~"), ".ample" ),
                            'run_dir' : os.getcwd(),
                            'scwrl_exe' : None,
                            'sf_cif' : None,
                            'shelx_cycles' : 15,
                            'shelxe_exe' : None,
                            'shelxe_rebuild' : False,
                            'SIGF' : None,
                            'spicker_exe' : None,
                            'split_mr' : False,
                            'submit_array' : True,
                            'submit_cluster' : False,
                            'submit_qtype' : None,
                            'theseus_exe' : None,
                            'top_model_only' : False,
                            'transmembrane' : False,
                            'transmembrane_octopusfile' : None,
                            'transmembrane_lipofile' : None,
                            'transmembrane_spanfile' : None,
                            'truncation_method' : 'percent',
                            'use_arpwarp' : True,
                            'use_buccaneer' : True,
                            'use_homs' : True,
                            'use_scwrl' : False,
                            'use_shelxe' : True,
                         }

        self.quick_mode = {
                           'max_ensemble_models' : 10,
                           'nmodels' : 200,
                           'percent' : 20,
                           'molrep_only' : False,
                           'phaser_only' : True,
                           'shelx_cycles' : 5,
                           'use_arpwarp' : False,
                           'use_buccaneer' : False,
                           'phaser_kill' : 15
                        }

        # Test use scrwl
        self.devel_mode = {
                           'early_terminate': False,
                           'benchmark_mode': True,
                           'use_shelxe' : True,
                           'shelxe_rebuild' : True,
                           'use_scwrl' : False,
                           'use_arpwarp' : False,
                           'use_buccaneer' : False,
                           # This kills phaser after 6 hours
                           'phaser_kill' : 360,
                           #'mr_keys' : [ [ 'PKEY', 'KILL','TIME','360'  ] ],
                        }

        # We have a debug mode as the logger isn't activated when we run
        self.debug = False

        return
    
    def populate( self, parser_args ):
        """
        Fill ourselves with the options from the parser
        """

        tmpv = None
        for k, v in vars(parser_args).iteritems():
            #print "{} | {}".format( k, v )
            if isinstance(v,list):
                # All values are in a list
                tmpv  = v[0]
            else:
                tmpv = v

            # Bit of a hack for true/false
            if isinstance( tmpv, str ):
                if tmpv.lower() == "true":
                    tmpv = True
                elif tmpv.lower() == "false":
                    tmpv = False

            self.d[k] = tmpv
        # end of loop

#        print "After populate"
#        for k, v in self.d.iteritems():
#            print "{} | {}".format( k, v )

        # Handle any defaults and any preset options
        self.process_options()

        return

    def process_options(self):
        """Check the options and process any preset defaults"""
        
        # Add the version
        self.d['ample_version']=version.__version__

        # First set anything that hasn't been set to its default option
        for k, v in self.defaults.iteritems():
            if k not in self.d:
                self.d[k] = v
            elif  self.d[k] == None:
                #if self.debug:
                #    print "Setting default value: {0} : {1}".format(k,v)
                self.d[k] = v
            else:
                if self.debug and self.d[k] != v:
                    print "Changed default value: {0} : {1}".format(k, self.d[k])

        # Any changes here
        if self.d['submit_qtype']:
            self.d['submit_qtype'] = self.d['submit_qtype'].upper()


        # Convert all paths to absolute paths
        paths = [
                 'alignment_file',
                'blast_dir',
                'domain_all_chains_pdb',
                'ensembles_dir',
                'fasta',
                'frags_3mers',
                'frags_9mers',
                'import_cluster',
                'maxcluster_exe',
                'models_dir',
                'mr_sequence',
                'mtz',
                'native_pdb',
                'NMR_model_in',
                'NMR_remodel_fasta',
                'psipred_ss2',
                'quark_models',
                'rosetta_db',
                'rosetta_dir',
                'rosetta_fragments_exe',
                'rosetta_AbinitioRelax',
                'scwrl_exe',
                'sf_cif',
                'shelxe_exe',
                'spicker_exe',
                'theseus_exe',
                'transmembrane_octopusfile',
                'transmembrane_lipofile',
                'transmembrane_spanfile'
            ]
        for k, v in self.d.iteritems():
            if k in paths and isinstance( v, str ):
                self.d[ k ] = os.path.abspath( v )

        # Check if using any preset options
        if self.d['devel_mode']:
            for k, v in self.devel_mode.iteritems():
                # Set any that haven't been set
                if self.d[k] == None:
                    self.d[k] = v
                else:
                    # Already set - only overwrite if it's set to a default value, otherwise we
                    # let the user go with what they've chosen but warn
                    if self.d[k] != self.defaults[k] and self.d[k] != v  :
                        print "WARNING! Overriding devel_mode setting: {0} : {1} with user setting {2}".format( k, v, self.d[k] )
                    else:
                        # We overwrite the default with our value
                        if self.debug:
                            print "Overriding default setting: {0} : {1} with devel_mode setting {2}".format( k, self.defaults[k], v )
                        self.d[k] = v

        if self.d['quick_mode']:
            for k, v in self.quick_mode.iteritems():
                # Set any that haven't been set
                if self.d[k] == None:
                    self.d[k] = v
                else:
                    # Already set - only overwrite if it's set to a default value, otherwise we
                    # let the user go with what they've chosen but warn
                    if self.d[k] != self.defaults[k] and self.d[k] != v  :
                        print "WARNING! Overriding quick_mode setting: {0} : {1} with user setting {2}".format( k, v, self.d[k] )
                    else:
                        # We overwrite the default with our value
                        if self.debug:
                            print "Overriding default setting: {0} : {1} with quick_mode setting {2}".format( k, self.defaults[k], v )
                        self.d[k] = v

        return

    def prettify_parameters(self):
        """
        Return the parameters nicely formated as a list of strings suitable for writing out to a file
        """
        pstr = ""
        pstr +='Params Used in this Run\n\n'

        keys1 = ['fasta','work_dir','mtz','name']
        pstr += '---input---\n'
        for k in keys1:
            pstr += "{0}: {1}\n".format(k, self.d[k])

        keys2 = ['make_frags','rosetta_fragments_exe','frags_3mers','frags_9mers']
        pstr+= '\n---fragments---\n'
        for k in keys2:
            pstr += "{0}: {1}\n".format(k, self.d[k])

        keys3 = ['make_models','rosetta_AbinitioRelax','rosetta_db']
        pstr+= '\n---modelling---\n'
        for k in keys3:
            pstr += "{0}: {1}\n".format(k, self.d[k])

        if self.d['use_scwrl']:
            pstr+= '\n---3rd party---\nSCWRL {0}\n'.format( self.d['scwrl_exe'] )

        keys4 = ['missing_domain','domain_all_chains_pdb']
        if keys4[0]:
            pstr+= '\n---Missing Domain---\n'
            for k in keys4:
                pstr += "{0}: {1}\n".format(k, self.d[k])

        # This only used for printing
        INSERT_DOMAIN = False
        if self.d['domain_termini_distance'] > 0:
            INSERT_DOMAIN = True
        pstr += '\nIs an Insert Domain {0} termini distance {1}\n'.format( INSERT_DOMAIN, self.d['domain_termini_distance'] )

        # Now print out everything else
        pstr += "\n---Other parameters---\n"

        done_keys = keys1 + keys2 + keys3 + keys4 + [ 'use_scwrl', 'domain_termini_distance'  ]
        for k, v in sorted(self.d.items()):
            if k not in done_keys:
                pstr += "{0} : {1}\n".format( k, v )

        return pstr
                dom = request.form.get('domain')
                fromzone = request.form.get('fromzone')
                tozone = request.form.get('tozone')
                direction = request.form.get('direction')
                action = request.form.get('action')
                description  = request.form.get('description')
                ethertype= request.form.get('ethertype')
                protocol= request.form.get('protocol')
                sourceport = request.form.get('sourceport')
                destinationport = request.form.get('destinationport')
                dscp = request.form.get('dscp')


                #Get the domain
                domain = nuage_user.domains.get_first(filter="name == '%s'" % dom)
                                domain.fetch()
                # Creating the job to begin the policy changes
                job = vsdk.NUJob(command='BEGIN_POLICY_CHANGES')
                domain.create_child(job)
                # wait for the job to finish
                while True:
                    job.fetch()
                    if job.status == 'SUCCESS':
                        break
                    if job.status == 'FAILED':
                        return render_template('fail_acls.html', domain = domain)
                        break
                    time.sleep(1)# can be done with a while loop

                from_network = domain.zones.get_first(filter="name == '%s'" % fromzone)
                to_network = domain.zones.get_first(filter="name == '%s'" % tozone)

                for in_acl in domain.ingress_acl_templates.get():
                    ingressacl = in_acl
                for out_acl in domain.egress_acl_templates.get():
                    egressacl = out_acl

                if direction == 'Ingress':
                    db_ingressacl_rule = vsdk.NUIngressACLEntryTemplate(
                        action=action,
                        description=description,
                        ether_type=ethertype,
                        location_type='ZONE',
                        location_id=from_network.id,
                        network_type='ZONE',
                        network_id=to_network.id,
                        protocol=protocol,
                        source_port=sourceport,
                        destination_port=destinationport,
                        dscp=dscp
                        )
                    ingressacl.create_child(db_ingressacl_rule)
                if direction == 'Egress':
                    db_ingressacl_rule = vsdk.NUEgressACLEntryTemplate(
                        action=action,
                        description=description,
                        ether_type=ethertype,
                        location_type='ZONE',
                        location_id=from_network.id,
                        network_type='ZONE',
                        network_id=to_network.id,
                        protocol=protocol,
                        source_port=sourceport,
                        destination_port=destinationport,
                        dscp=dscp
                        )
                    egressacl.create_child(db_egressacl_rule)

                # Applying the changes to the domain
                job = vsdk.NUJob(command='APPLY_POLICY_CHANGES')
                dom.create_child(job)
                while True:
                    job.fetch()
                    if job.status == 'SUCCESS':
                        break
                    if job.status == 'FAILED':
                        return render_template('fail_acls.html', domain = domain)
                        break
                    time.sleep(1)# can be done with a while loop
                return render_template('add_acl_success.html')
